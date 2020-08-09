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

Inside the container, go to the `common-crawl` folder and run the following (while replacing the `wet.paths.gz` and
joblog path):

```bash
cd common-crawl
aws s3 cp --no-sign-request s3://commoncrawl/crawl-data/CC-MAIN-2020-29/wet.paths.gz - | gzip -d \
    parallel --joblog /tmp/commoncrawl-joblog --bar ./filter_wet.py {} > /tmp/filtered-output.wet
```

You can additionally add:
 - `--resume` - if the process was interrupted and you want to continue where you left off
 - `--resume-failed` - if there are failed jobs that you want to re-run
