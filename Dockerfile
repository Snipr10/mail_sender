FROM python:3.9-slim-buster
# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


COPY requirements.txt /usr/src/app/requirements.txt
RUN apt install python3-pip
RUN apt apt-key adv --recv-keys --keyserver keyserver.ubuntu.com 0xcbcb082a1bb943db
RUN curl -LsS https://downloads.mariadb.com/MariaDB/mariadb_repo_setup | sudo bash
RUN apt-get install -y apt-transport-https
RUN apt-get
RUN apt-get upgrade
RUN apt-get dist-upgrade
RUN apt-get install libmariadb3
RUN apt-get install libmariadb-dev
RUN pip3 install -r requirements.txt

# copy project
COPY . /usr/src/app/
