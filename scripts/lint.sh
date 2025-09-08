#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

SCRIPT_DIR="$(dirname "$0")"

set -x
pre-commit run --all-files --show-diff-on-failure

docker compose exec -T web python manage.py spectacular --file /tmp/schema.yaml --validate

"$SCRIPT_DIR"/validate_mkdocs.sh
