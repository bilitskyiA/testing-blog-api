FROM python:3.6
USER root
ENV PYTHONUNBUFFERED 1
RUN mkdir /backend
WORKDIR /backend
ADD requirements.txt /backend
RUN ln -s /usr/lib/x86_64-linux-gnu/libz.so /lib/
RUN ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /lib/
RUN apt-get update && apt-get install -y \
    python3-dev \
    python3-setuptools \
    libxml2-dev \
    libxslt-dev \
    libjpeg-dev \
    libffi-dev \
    gcc \
    musl-dev
RUN pip install -r requirements.txt
ADD . /backend
