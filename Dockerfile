FROM python:3.10.10-slim-buster
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apt-get update
RUN apt-get install -y postgresql postgresql-contrib gcc python3-dev musl-dev
RUN pip install --upgrade pip
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
EXPOSE 8000
COPY . .
