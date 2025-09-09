#!/bin/bash
set -euo pipefail
IFS=$'\n\t'
set -x

pre-commit run --all-files --show-diff-on-failure

docker compose exec -T web python manage.py spectacular --file /tmp/schema.yaml --validate
