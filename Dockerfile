FROM ubuntu:focal

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
RUN ln -sf /usr/bin/python3 /usr/bin/python && \
    ln -sf /usr/bin/pip3 /usr/bin/pip
    
COPY . /app
WORKDIR /app
RUN pip install .
