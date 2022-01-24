# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /code

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY /code .
CMD ["uvicorn", "--host", "0.0.0.0", "main:app"]