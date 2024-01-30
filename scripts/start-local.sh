#!/bin/bash
# Called by start-dev.sh and start-docker.sh, which sets
#    - DATABASE_HOST
#    - DJANGO_SUPERUSER
#    - DJANGO_SUPERUSER_PASSWORD
#    - DJANGO_SUPERUSER_EMAIL
if [[ $PWD != *"app"* ]]; then
    # shellcheck disable=SC2164
    cd app
    # shellcheck disable=SC2181
    if [[ $? != 0 ]]; then
        echo "ERROR: cd app failed"
        return 1
    fi
fi

# shellcheck disable=SC1091
source ../scripts/loadenv.sh
# shellcheck disable=SC2181
if [[ $? != 0 ]]; then
    echo "ERROR: loadenv.sh failed"
    return 1
fi
if [[ "$DJANGO_SETTINGS_MODULE" == "" ]]; then
    echo "ERROR: DJANGO_SETTINGS_MODULE not set"
    return 1
fi
echo Admin user = "$DJANGO_SUPERUSER" email = "$DJANGO_SUPERUSER_EMAIL"
if [[ $1 != "" ]]; then
    port=$1
elif [[ "$DJANGO_PORT" != "" ]]; then
    port=$DJANGO_PORT
else
    port=8000
fi
echo Port is "$port"
echo DJANGO_SETTINGS_MODULE "$DJANGO_SETTINGS_MODULE"

echo
echo --- Executing python manage.py makemigrations ---
echo
python manage.py makemigrations

# shellcheck disable=SC2181
if [[ $? != 0 ]]; then
    echo "ERROR: python manage.py makemigrations failed"
    return 1
fi

echo
echo --- Executing python manage.py migrate ---
echo
python manage.py migrate
# shellcheck disable=SC2181
if [[ $? != 0 ]]; then
    echo "ERROR: python manage.py migrate failed"
    return 1
fi

echo
echo --- Executing python manage.py shell to check if "$DJANGO_SUPERUSER_USERNAME" exists
echo
python manage.py shell -c "from core.models import User; exists = (User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists()); sys.exit(0 if exists else 1)"
# shellcheck disable=SC2181
superuser_exists=$?

if [ $superuser_exists -eq 1 ]; then
  echo
  echo --- Executing python manage.py createsuperuser ---
  echo
  python manage.py createsuperuser --username "$DJANGO_SUPERUSER_USERNAME" --email "$DJANGO_SUPERUSER_EMAIL" --no-input
else
  echo --- INFO: Skipping python manage.py createsuperuser - super user "$DJANGO_SUPERUSER_USERNAME" already exists.
fi

# shellcheck disable=SC2181
if [[ $? != 0 ]]; then
    echo "ERROR: python manage.py createsuperuser failed"
    return 1
fi

echo
echo --- All prep steps successful!  Executing python manage.py runserver
echo

python manage.py runserver 0.0.0.0:"$port"
