#!/bin/bash
set -eux

# build mkdocs with validation, and don't worry about the output
if [ "$SKIP_MKDOCS_VALIDATION" != "true" ]; then
    echo "Skipping mkdocs validation"
    exit 0
fi
docker-compose exec -T mkdocs sh -c "mkdocs build -d /tmp --strict"
