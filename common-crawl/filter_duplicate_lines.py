#!/usr/bin/env python
import warc
import argparse
from pybloomfilter import BloomFilter
import sys

parser = argparse.ArgumentParser("Filter lines that exists in a bloom filter")
parser.add_argument("bloom_filter", help="Path to saved bloom filter")
parser.add_argument("--verbose", action="store_true")

params = parser.parse_args()

input_warc_file = warc.WARCFile(fileobj=sys.stdin.buffer, mode="rb")
output_warc_file = warc.WARCFile(fileobj=sys.stdout.buffer, mode="wb")

bf = BloomFilter.open(params.bloom_filter, mode="rb")

num_skipped = 0
num_lines = 0
for record in input_warc_file:
    output_payload = b''
    for line in record.payload:
        num_lines += 1
        if line not in bf:
            output_payload += line
        else:
            num_skipped += 1
    output_warc_file.write_record(warc.WARCRecord(record.header, output_payload, defaults=False))

if params.verbose:
    sys.stderr.write(f"Duplicate filter: Removed {num_skipped} lines ({num_skipped * 100 / num_lines:.2f}%)\n")