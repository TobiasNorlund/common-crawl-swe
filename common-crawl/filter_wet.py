desc="""
Script to download and parse a common crawl WET file and filter out all documents where the identified
languages includes swedish (swe), and output these to stdout
"""

import os
import sys
import warc
import boto3
import tempfile
import logging
import argparse
from urllib.parse import urlparse

parser = argparse.ArgumentParser(desc)
parser.add_argument("s3_wet_file", help="s3 path to wet file")
parser.add_argument("--verbose", action="store_true", default=False)
params = parser.parse_args()

logging.basicConfig(stream=sys.stderr, level=logging.INFO if params.verbose else logging.ERROR,
                    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

def record_filter_predicate(record: warc.WARCRecord):
    """
    Return True if record is to be kept, otherwise False
    """
    return "WARC-Identified-Content-Language" in record.header and \
           "swe" in record.header["WARC-Identified-Content-Language"]


def parse_s3_path(s3_path):
    parse_result = urlparse(s3_path)
    return parse_result.netloc or "commoncrawl", parse_result.path

# Create s3 client
s3 = boto3.client("s3")

# Setup output writer (to stdout)
out = warc.WARCFile(fileobj=sys.stdout.buffer, mode="wb")

# Download the file
bucket, object = parse_s3_path(params.s3_wet_file)
with tempfile.NamedTemporaryFile(mode="wb", suffix=os.path.basename(object)) as temp_wet_file:
    logging.info(f"Downloading '{object}' into '{temp_wet_file.name}' ...")
    s3.download_fileobj(bucket, object, temp_wet_file)

    wet_parser = warc.WARCFile(filename=temp_wet_file.name)
    for i, record in enumerate(wet_parser):
        # If record passes filter, write it to stdout
        if record_filter_predicate(record):
            out.write_record(record)
