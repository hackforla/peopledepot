#!/bin/bash
set -eux

# build mkdocs with validation, and don't worry about the output
docker-compose exec -T mkdocs sh -c "mkdocs build -d /tmp --strict"
