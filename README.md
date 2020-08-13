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
cd common-crawl
aws s3 cp --no-sign-request s3://commoncrawl/crawl-data/CC-MAIN-2020-29/wet.paths.gz - | gzip -d \
    parallel --joblog /tmp/commoncrawl-joblog --bar --resume --resume-failed \
        aws s3 cp --no-sign-request s3://commoncrawl/{} - '|' gzip -d '|' ./filter_language.py swe > /tmp/filtered-output.wet
```

 - `--resume` - continues where you left off if the process was previously interrupted
 - `--resume-failed` - if there are failed jobs that you want to re-run
