FROM ubuntu:18.04

WORKDIR /opt
COPY . /opt

USER root

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get -o Acquire::Check-Valid-Until=false -o Acquire::Check-Date=false update -y
RUN apt-get update
RUN apt-get install -y python3.6-dev \
                       python3-pip \
                       wget \
                       build-essential \
                       software-properties-common \
                       apt-utils \
       
RUN pip3 install requirements.txt -y
RUN ldconfig

ENTRYPOINT [ "/usr/bin/python3", "/opt/3d_soil_mask.py" ]
