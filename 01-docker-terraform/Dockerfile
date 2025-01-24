FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ingest_data.py ingest_data.py