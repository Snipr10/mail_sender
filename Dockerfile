FROM python:3.9.13-alpine3.16
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
