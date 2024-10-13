FROM python:3.12

RUN apt-get update && apt-get install -y git jq

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
