FROM python:3.12

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y git vim fonts-roboto libfreetype6-dev libpng-dev
RUN pip install .

ENTRYPOINT ["python", "igo"]
