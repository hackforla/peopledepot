#!/bin/bash
set -euo pipefail
IFS=$'\n\t'
set -x

# run tests and show code coverage
docker-compose exec -T web pytest
