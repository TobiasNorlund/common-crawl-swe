FROM python:3.7

RUN apt update && apt install -y parallel
COPY bash.bashrc /etc/bash.bashrc

WORKDIR /opt/project

RUN pip install warc3-wet \
				boto3 \
				tqdm \
				awscli