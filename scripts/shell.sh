#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

echo "\q to quit"

set -x
docker-compose exec web run /bin/sh -e .env.docker
