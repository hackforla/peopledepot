#!/bin/bash
set -euo pipefail
IFS=$'\n\t'
set -x

# generate requirements.txt with the latest package versions
docker compose exec web uv pip compile -o requirements.txt requirements.in --no-header --upgrade

# generate requirements-aws.txt with the latest package versions
docker compose exec web uv pip compile -o requirements-aws.txt requirements-aws.in --no-header --upgrade --python-version 3.10
