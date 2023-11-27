#!/bin/bash
set -euo pipefail
IFS=$'\n\t'
set -x

# create and run any migrations
docker-compose exec -T web python manage.py makemigrations
docker-compose exec -T web python manage.py migrate "$@"
