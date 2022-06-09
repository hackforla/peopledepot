#!/bin/bash
set -x

# clean, build, and run in background
docker-compose down -v --remove-orphans
docker-compose up -d --build
./migrate.sh
./createsuperuser.sh
