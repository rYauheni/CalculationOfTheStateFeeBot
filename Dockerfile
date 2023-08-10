FROM python:3.10-alpine3.15

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN pip install --upgrade pip

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8000
