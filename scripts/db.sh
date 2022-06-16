#!/bin/bash
set -x

echo "\q to quit"

docker-compose exec db psql -d people_depot_dev -U people_depot
