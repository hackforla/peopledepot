#!/bin/sh

python manage.py migrate --noinput

exec gunicorn peopledepot.wsgi:application --bind 0.0.0.0:8000
