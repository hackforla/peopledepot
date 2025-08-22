#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

set -x
docker-compose exec -e .env.docker web /bin/sh
