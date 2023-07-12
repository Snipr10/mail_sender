
FROM python:3.8

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# RUN apt-key adv --recv-keys --keyserver keyserver.ubuntu.com 0xcbcb082a1bb943db
# RUN curl -LsS https://downloads.mariadb.com/MariaDB/mariadb_repo_setup | bash
RUN apt-get install -y apt-transport-https
COPY requirements.txt /usr/src/app/requirements.txt
RUN apt-get install -y libmariadb3
RUN apt-get install -y libmariadb-dev

RUN pip3 install --upgrade pip
RUN pip3 install mariadb==1.1.7
RUN pip3 install -r requirements.txt

# copy project
COPY . /usr/src/app/
