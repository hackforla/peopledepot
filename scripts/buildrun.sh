#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

SCRIPT_DIR="$(dirname "$0")"
# https://codefather.tech/blog/bash-get-script-directory/

# clean, build, and run in background
# c     Delete docker containers and networks
# v    *Remove docker volumes
# o    *Remove docker orphan containers
# d     Run in background
# b     Rebuild
# m     Run migrations
# s     Create superuser
# l     Tail logs after run
set -x
"$SCRIPT_DIR"/run.sh -c -o -d -b -m "$@"
