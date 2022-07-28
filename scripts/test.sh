#!/bin/bash
set -x

# run tests and show code coverage
docker-compose exec web pytest -p no:warnings --cov-report html --cov=.
