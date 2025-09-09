#!/bin/bash
set -euo pipefail
IFS=$'\n\t'
set -x

# tail all container logs
# pass in service name to filter by service. e.g. ./logs.sh web
docker compose logs -f "$@"
