# Common Crawl filter scripts

The purpose of this repo is to provide some scripts for easily filter WET records from CommonCrawl archives.

First, build the docker image:

```bash
$ ./scripts/build.sh
```

then, launch a container with:

```bash
$ ./scripts/run.sh
```

Inside the container, go to the `common-crawl` folder and run the following (while replacing the `wet.paths.gz`,
joblog and output paths):

```bash
aws s3 cp --no-sign-request s3://commoncrawl/crawl-data/CC-MAIN-2020-29/wet.paths.gz - | gzip -d \
    parallel --joblog /tmp/commoncrawl-joblog --bar --resume --resume-failed \
        aws s3 cp --no-sign-request s3://commoncrawl/{} - '|' gzip -d '|' ./filter_language.py swe >> /tmp/filtered-output.wet
```

 - `--resume` - continues where you left off if the process was previously interrupted
 - `--resume-failed` - if there are failed jobs that you want to re-run
 - `--jobs 16` - To set custom amount of parallel jobs
 
## Example script to download and pre-process CC-MAIN-2020-29 on a machine with many cores

```bash
##  Download archive and do initial language filter
mkdir -p ../data/CC-MAIN-2020-29
aws s3 cp --no-sign-request s3://commoncrawl/crawl-data/CC-MAIN-2020-29/wet.paths.gz - | gzip -d | \
    parallel --joblog ../data/CC-MAIN-2020-29/joblog --bar --resume --resume-failed --jobs 64 \
        aws s3 cp --no-sign-request s3://commoncrawl/{} - '|' gzip -d '|' ./filter_language.py swe > ../data/CC-MAIN-2020-29/data.swe.wet

## Build bloom filter to filter duplicates
NUM_LINES=$(wc -l ../data/CC-MAIN-2020-29/data.swe.wet)
cat ../data/CC-MAIN-2020-29/data.swe.wet | tqdm --bytes | ./build_bloom_filter.py --output /dev/shm/filter.bloom --capacity $NUM_LINES --false-positive-prob 1e-4

## Remove duplicate lines and filter short records
cat ../data/CC-MAIN-2020-29/data.swe.wet | tqdm --bytes | ./filter_duplicate_lines.py /dev/shm/filter.bloom | ./filter_record_length.py --min-length 1024 | gzip > ../data/CC-MAIN-2020-29/data.swe.dedup.wet.gz
```
