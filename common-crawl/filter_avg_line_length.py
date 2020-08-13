#!/usr/bin/env python
import warc
import argparse
import sys
import statistics

parser = argparse.ArgumentParser("Filter records whose average line length is shorter than a specified threshold")
parser.add_argument("threshold", type=int)
params = parser.parse_args()

def record_filter_predicate(payload):
    """
    Return True if record is to be kept, otherwise False
    """
    line_lengths = [len(line)
                    for line in payload.decode("utf-8").split("\n")]
    return statistics.mean(line_lengths) > params.threshold

input_warc_file = warc.WARCFile(fileobj=sys.stdin.buffer, mode="rb")
output_warc_file = warc.WARCFile(fileobj=sys.stdout.buffer, mode="wb")

for record in input_warc_file:
    payload = record.payload.read()
    if record_filter_predicate(payload):
        output_warc_file.write_record(warc.WARCRecord(record.header, payload, defaults=False))
