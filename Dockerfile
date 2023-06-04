FROM python:3.9

RUN pip install uvicorn
RUN pip install uvicorn[standard]
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src /src
WORKDIR src

CMD ["uvicorn", "service:app", "--host", "0.0.0.0", "--port", "8080"]