FROM python:3.6
ENV PYTHONUNBUFFERED 1

RUN apt update && apt install postgresql-client gettext -y

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
COPY . /app
WORKDIR /app
