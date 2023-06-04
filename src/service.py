import pandas as pd
from fastapi import FastAPI, Request
import mlflow

preprocessor = None
model = None
try:
    mlflow_client = mlflow.tracking.MlflowClient()

    # Get latest preprocessor.
    preprocessors = mlflow_client.search_runs(
        ["0"], "run_name LIKE 'preprocessor'",
        order_by=["start_time DESC"],
        max_results=1)
    preprocessor = \
        mlflow.sklearn.load_model(f"runs:/{preprocessors[0].info.run_id}/model")

    # Get model with lowest RMSE.
    runs = mlflow_client.search_runs(
        ["0"], "", order_by=["metrics.rmse"], max_results=1)
    model = mlflow.pyfunc.load_model(f"runs:/{runs[0].info.run_id}/model")

    print('Model loaded!')
except Exception as e:
    print('Model loading failed:', e)

app = FastAPI()


@app.get("/")
async def root():
    return {'preprocessor': dict(preprocessors[0].info),
            'model': dict(runs[0].info)}


@app.post("/predict")
async def model_predict(request: Request):
    df_x = pd.DataFrame(await request.json())
    df_x_scaled = preprocessor.transform(df_x)
    return pd.DataFrame(model.predict(df_x_scaled))
