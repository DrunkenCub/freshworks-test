FROM python:3.8-slim-buster

WORKDIR /usr/src/app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y && \
    apt-get install -y python-pip libpq-dev python-dev

# install dependencies
RUN pip install --upgrade pip


COPY . /usr/src/app/

RUN pip install -r req.txt