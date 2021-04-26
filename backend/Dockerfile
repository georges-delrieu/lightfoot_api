FROM python:3.8-slim-buster
WORKDIR /backend
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc postgresql \
  && apt-get clean
# install python dependencies
RUN apk --no-cache add build-base
RUN apk --no-cache add postgresql-dev
RUN python3 -m pip install psycopg2
RUN pip install --upgrade pip
COPY ./requirements.txt /backend/requirements.txt
RUN pip install -r requirements.txt
COPY . /backend