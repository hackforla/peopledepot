#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

set -x
docker-compose exec web python manage.py rebase_migration core
