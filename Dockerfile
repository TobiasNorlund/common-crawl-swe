FROM python:3.7

RUN apt update && apt install -y parallel less
COPY bash.bashrc /etc/bash.bashrc

WORKDIR /opt/project/common-crawl

# For the bloom filters to work across python sessions
ENV PYTHONHASHSEED=0

RUN pip install warc3-wet \
				boto3 \
				tqdm \
				awscli \
				pybloomfiltermmap3