#!/bin/bash

SCRIPTS_DIR="$(dirname "$0")"
source "$SCRIPTS_DIR/common.sh"

USER_MAP="-u $(id -u):$(id -g)"

set -x
docker run --rm -it \
  -v $PROJECT_ROOT:/opt/project \
  -v /tmp:/tmp \
  -v $HOME/.aws:/.aws \
  $USER_MAP \
  $DOCKER_IMAGE_NAME bash
