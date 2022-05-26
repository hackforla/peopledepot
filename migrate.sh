#!/bin/bash
set -x

# create and run any migrations
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
