FROM ubuntu:20.04 AS development
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update;\
    apt-get install -y python3-pip ffmpeg libsm6 libxext6

COPY ./requirements.txt /usr/src/app/
RUN pip3 install -r /usr/src/app/requirements.txt

ENV PYTHONUNBUFFERED 1
