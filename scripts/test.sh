#!/bin/bash
set -euo pipefail
IFS=$'\n\t'
set -x

# check for missing migration files
# https://adamj.eu/tech/2024/06/23/django-test-pending-migrations/
docker-compose exec -T web python manage.py makemigrations --check

# run tests and show code coverage
# filter tests using -k <filter>
# ex: test.sh -k program_area --no-cov
docker-compose exec -T web pytest "$@"
