#!/usr/bin/env python
import warc
import argparse
import sys

parser = argparse.ArgumentParser("Filters whole WARC records based on the payload length")
parser.add_argument("--min-length", type=int, default=0)
parser.add_argument("--max-length", type=int, default=1e9)

params = parser.parse_args()

def record_filter_predicate(record: warc.WARCRecord):
    return params.min_length < int(record.header["Content-Length"]) < params.max_length


input_warc_file = warc.WARCFile(fileobj=sys.stdin.buffer, mode="rb")
output_warc_file = warc.WARCFile(fileobj=sys.stdout.buffer, mode="wb")

for record in input_warc_file:
    if record_filter_predicate(record):
        output_warc_file.write_record(record)
