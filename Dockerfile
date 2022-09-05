FROM docker.io/library/python:3.8-slim

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /tmp/
ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt update && apt install -y gnupg2 curl
RUN apt install -y unixodbc unixodbc-dev

RUN apt update && apt install postgresql-client -y
RUN apt install --reinstall -y build-essential
RUN apt autoremove -y

COPY . /src

RUN pip install --no-cache-dir -r /tmp/requirements.txt
WORKDIR /src

# ENV PYTHONPATH /src/

EXPOSE 8000
