desc="""
Script to fun "filter_wet.py" for each wet file in a common crawl archive, in parallel
"""

import argparse
import logging
import sys
import zlib
import boto3
import concurrent.futures
import subprocess
import tqdm
from botocore.config import Config
from botocore import UNSIGNED
from utils import TqdmLoggingHandler

parser = argparse.ArgumentParser(desc)
parser.add_argument("archive_name", help="Common Crawl archive name, e.g. 'CC-MAIN-2017-04'")
parser.add_argument("output_file", help="Output file path")
parser.add_argument("--num-processes", type=int, default=None)
params = parser.parse_args()

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', handlers=[TqdmLoggingHandler()])


def process_wet(wet_path):
    """
    Executes the filter_wet.py script in a subprocess for the specific wet_path
    :return: The stdout of the filter_wet.py script
    """
    command = ["python", "filter_wet.py", wet_path]
    logging.info(f"Starting processing of '{wet_path}'")
    res = subprocess.run(command, capture_output=True)
    res.check_returncode()
    return res.stdout


def get_wet_files(archive_name):
    s3 = boto3.resource('s3', config=Config(signature_version=UNSIGNED))
    obj = s3.Object("commoncrawl", f"crawl-data/{archive_name}/wet.paths.gz")
    compressed_data = obj.get()['Body'].read()
    return zlib.decompress(compressed_data, 16+zlib.MAX_WBITS).decode("utf-8").split()


wet_paths = get_wet_files(params.archive_name)
logging.info(f"Found {len(wet_paths)} WET files for archive {params.archive_name}")

with concurrent.futures.ThreadPoolExecutor(max_workers=params.num_processes) as executor, \
        open(params.output_file, "wb") as output_file:
    # Submit a job for each wet file
    future_to_wet_path = {executor.submit(process_wet, wet_path): wet_path for wet_path in wet_paths}
    for future in tqdm.tqdm(concurrent.futures.as_completed(future_to_wet_path), total=len(wet_paths)):
        wet_path = future_to_wet_path[future]
        try:
            wet_records = future.result()
            output_file.write(wet_records)
        except Exception as exc:
            logging.error(f"Path {wet_path} generated an exception: {exc}")
        else:
            logging.info(f"Path {wet_path}' finished successfully!")