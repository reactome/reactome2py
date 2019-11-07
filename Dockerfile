FROM ubuntu:18.04

RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    python3 \
    python3-setuptools \
    python3-pip \
    python3-dev \
    pandoc \
    libssl-dev \
    libcurl4-openssl-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip
RUN pip install pandas argparse requests json csv jupyterlab --upgrade 
RUN ln -s /usr/bin/python3 /usr/bin/python && \ 
    ln -s /usr/bin/pip3 /usr/bin/pip
    
COPY . /app/

WORKDIR /app

RUN python setup.py install
