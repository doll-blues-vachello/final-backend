FROM python:3.9-bullseye

COPY ./requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app