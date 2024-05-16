#!/bin/bash
set -euo pipefail
IFS=$'\n\t'
set -x

# generate requirements.txt with the latest package versions
docker-compose exec web uv pip compile -o requirements.txt requirements.in --no-header --upgrade
