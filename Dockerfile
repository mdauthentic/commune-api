FROM python:3.8-slim-buster

WORKDIR /commune-api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /commune-api/requirements.txt
RUN pip install -r requirements.txt

COPY . /commune-api

