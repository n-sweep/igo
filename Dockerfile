FROM python:3.12

WORKDIR /app

COPY . .

RUN apt-get update && \
    apt-get install -y git chromium vim fonts-roboto fonts-noto-color-emoji libfreetype6-dev libpng-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt-lists/*
RUN pip install .

ENTRYPOINT ["python", "igo"]
