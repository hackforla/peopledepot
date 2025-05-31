#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

SCRIPT_DIR="$(dirname "$0")"
# https://codefather.tech/blog/bash-get-script-directory/

usage() {
  echo "Runs PeopleDepot dev build with options"
  echo
  echo "Syntax: $0 [-h|c|v|o|d|b|m|s|l]"
  echo "options:"
  echo "h     Show usage"
  echo "c     Delete docker containers and networks."
  echo "v     Remove docker volumes."
  echo "o     Remove docker orphan containers."
  echo "d     Run in background."
  echo "b     Rebuild"
  echo "m     Run migrations"
  echo "s     Create superuser"
  echo "l     Tail logs after run."
  echo
}

exit_abnormal() {
  usage
  exit 1
}

migrate() {
  # Run migrations
set -x
  "$SCRIPT_DIR"/migrate.sh
{ set +x; } 2>&-;
}

createsuperuser() {
  # Create superuser
set -x
  "$SCRIPT_DIR"/createsuperuser.sh
{ set +x; } 2>&-;
}

logs() {
  # Tail Logs
set -x
  "$SCRIPT_DIR"/logs.sh
{ set +x; } 2>&-;
}

dc_down() {
set -x
  docker-compose down "${DOWN_ARGS[@]}"
{ set +x; } 2>&-;
}

dc_up() {
set -x
  docker-compose up "${UP_ARGS[@]}"
{ set +x; } 2>&-;
}

DOWN_ARGS=()
UP_ARGS=()
DELETE_CONTAINERS=0
SHOW_LOGS=0
MIGRATE=0
CREATESUPERUSER=0

while getopts "lhdvobcms" option; do
  case $option in
    h)
      usage
      exit;;
    c) # delete containers and networks
      DELETE_CONTAINERS=1;;
    v) # remove volumes
      DOWN_ARGS+=(-v);;
    o) # remove orphans
      DOWN_ARGS+=(--remove-orphans);;
    d) # run in background
      UP_ARGS+=(-d);;
    b) # rebuild
      UP_ARGS+=(--build);;
    m) # run migrations
      MIGRATE=1;;
    s) # create superuser
      CREATESUPERUSER=1;;
    l) # tail logs
      SHOW_LOGS=1;;
    ?) # Invalid option
      echo "Invalid option: -${OPTARG}."
      exit_abnormal;;
  esac
done

if [ "$DELETE_CONTAINERS" = 1 ]; then
  dc_down
fi

dc_up

if [ "$MIGRATE" = 1 ]; then
  migrate
fi

if [ "$CREATESUPERUSER" = 1 ]; then
  createsuperuser
fi

if [ "$SHOW_LOGS" = 1 ]; then
  logs
fi
