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

COPY . /app/

WORKDIR /app

RUN python3 setup.py install

ENTRYPOINT ["reactome2py"]