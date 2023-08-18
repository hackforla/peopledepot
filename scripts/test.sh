#!/bin/bash
set -euo pipefail
IFS=$'\n\t'
set -x

# run tests and show code coverage
# filter tests using -k <filter>
# ex: test.sh -k program_area --no-cov
docker-compose exec -T web pytest "$@"
