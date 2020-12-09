FROM ubuntu:18.04

WORKDIR /opt
COPY . /opt

USER root

RUN apt-get update
RUN apt-get install -y python3.6-dev \
                       python3-pip \
                       wget \
                       build-essential \
                       software-properties-common \
                       apt-utils \
       
RUN pip3 install -r requirements.txt
RUN ldconfig

ENTRYPOINT [ "/usr/bin/python3", "/opt/3d_soil_mask.py" ]
