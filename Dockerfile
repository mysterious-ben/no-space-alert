FROM python:3.8.6-slim-buster
WORKDIR /app
COPY . /app
RUN apt-get update && apt-get install build-essential -y
RUN pip install --no-cache-dir -r requirements.txt
