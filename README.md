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

Inside the container, go to the `common-crawl` folder and run the `filter_archive.py` script:

```bash
docker-user /opt/project > cd common-crawl
docker-user /opt/project/common-crawl > python filter_archive.py CC-MAIN-2020-29 /tmp/CC-MAIN-2020-29.swe.wet
```

Voila!