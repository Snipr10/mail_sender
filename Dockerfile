FROM python:3.9.13-alpine3.16
RUN apk update
RUN apk add

RUN apk update --update libmariadb3

RUN apt-get install libmariadb3 libmariadb-dev


# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


COPY requirements.txt /usr/src/app/requirements.txt

RUN pip3 install mariadb
RUN pip3 install -r requirements.txt

# copy project
COPY . /usr/src/app/
