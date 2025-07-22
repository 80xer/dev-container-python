FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y less && rm -rf /var/lib/apt/lists/*
