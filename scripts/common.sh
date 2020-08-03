#!/bin/bash
export DOCKER_IMAGE_NAME=tobias/common-crawl-swe
export PROJECT_ROOT="$( dirname "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
export DATA_DIR="$PROJECT_ROOT/data"
