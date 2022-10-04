#!/bin/bash
set -euo pipefail
IFS=$'\n\t'
set -x

# run linters and code formatters

# https://github.com/hadolint/hadolint
# hadolint app/Dockerfile
docker run --rm -i hadolint/hadolint < app/Dockerfile

docker-compose exec -T web flake8 .

# docker-compose exec -T web black --check --exclude=migrations .
# docker-compose exec -T web black --diff --exclude=migrations .
docker-compose exec -T web black --exclude=migrations .

docker-compose exec -T web isort . --force-single-line-imports

docker-compose exec -T web python manage.py spectacular --file /tmp/schema.yaml --validate
