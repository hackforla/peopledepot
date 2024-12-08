#!/bin/bash
set -euo pipefail
IFS=$'\n\t'
set -x

# Create a test superuser for logging into django admin
# http://localhost:8000/admin/login

# This command requires the DJANGO_SUPERUSER_USERNAME and
# DJANGO_SUPERUSER_PASSWORD environmental variables to be set when django starts
echo "DJANGO_SUPERUSER_USERNAME: $DJANGO_SUPERUSER_USERNAME"
docker-compose exec web python manage.py createsuperuser --no-input
