#!/usr/bin/env python
import warc
import argparse
import sys

parser = argparse.ArgumentParser("Filters whole WARC records using the WARC-Identified-Content-Language header")
parser.add_argument("language")

params = parser.parse_args()

def record_filter_predicate(record: warc.WARCRecord):
    """
    Return True if record is to be kept, otherwise False
    """
    return "WARC-Identified-Content-Language" in record.header and \
           params.language == record.header["WARC-Identified-Content-Language"]

input_warc_file = warc.WARCFile(fileobj=sys.stdin.buffer, mode="rb")
output_warc_file = warc.WARCFile(fileobj=sys.stdout.buffer, mode="wb")

for record in input_warc_file:
    if record_filter_predicate(record):
        output_warc_file.write_record(record)
