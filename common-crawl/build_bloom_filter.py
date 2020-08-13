#!/usr/bin/env python
import argparse
import warc
import sys
from pybloomfilter import BloomFilter

# The idea is to use two bloom filters, one for all lines that appear at least once, and one for all lines that appear
# at least twice. Save only the second filter

parser = argparse.ArgumentParser()
parser.add_argument("--output", required=True)
parser.add_argument("--capacity", required=True, type=int)
parser.add_argument("--false-positive-prob", required=True, type=float)

params = parser.parse_args()

input_warc_file = warc.WARCFile(fileobj=sys.stdin.buffer, mode="rb")
bf1 = BloomFilter(params.capacity, params.false_positive_prob)
bf2 = BloomFilter(params.capacity, params.false_positive_prob, params.output)

num_lines = 0
num_duplicates = 0
for record in input_warc_file:
    for line in record.payload:
        # Only add lines to second bloom filter if already seen
        if line in bf1:
            bf2.add(line)
            num_duplicates += 1
        # Add all lines to first bloom filter
        bf1.add(line)
        num_lines += 1

sys.stderr.write(f"Found {num_duplicates} unique lines occurring at least twice (probably)\n")
