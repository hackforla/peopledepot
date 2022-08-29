#!/bin/bash

echo "\q to quit"

set -x
docker-compose exec db psql -d people_depot_dev -U people_depot
