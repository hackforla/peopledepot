#!/bin/bash
set -x

SCRIPT_DIR="$(dirname "$0")"
# https://codefather.tech/blog/bash-get-script-directory/

# clean, build, and run in background
docker-compose down -v --remove-orphans
docker-compose up -d --build

"$SCRIPT_DIR"/migrate.sh
# "$SCRIPT_DIR"/createsuperuser.sh
