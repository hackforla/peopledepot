#!/bin/bash
set -euo pipefail
IFS=$'\n\t'
set -x

# Check that there are not missing migrations
# --dry-run only prints the migration plan
# --check sets non-zero status code if migrations are missing
# --no-input disables any prompt
docker-compose exec -T web python manage.py makemigrations --dry-run --check --no-input
