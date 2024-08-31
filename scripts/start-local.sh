#!/bin/bash
# Called by start-dev.sh and start-docker.sh, which sets
#    - DATABASE_HOST
#    - DJANGO_SUPERUSER
#    - DJANGO_SUPERUSER_PASSWORD
#    - DJANGO_SUPERUSER_EMAIL
if [[ $PWD != *"app" ]]; then
    cd app || cd ../app ||
 {
        echo "ERROR: cd app failed.  Please run from the app directory."
        return 1
    }
fi

# pre-commit would cause this to fail.  We don't need the check for this script.
# shellcheck disable=SC1091
source ../scripts/loadenv.sh ||  {
    echo "ERROR: loadenv.sh failed"
    return 1
}

activate_venv() {
    # pre-commit would cause this to fail.  We don't need the check for this script.
    # shellcheck disable=SC1091
    source venv/bin/activate || {
        echo "ERROR: Failed to activate virtual environment"
        return 1
    }
}

if [ -z "$VIRTUAL_ENV" ]; then
    # Activate virtual environment or handle error
    activate_venv || return 1
fi

echo Admin user = "$DJANGO_SUPERUSER" email = "$DJANGO_SUPERUSER_EMAIL"
if [[ "$1" == "" ]]; then
    echo Setting port to param "$1"
    port=$1
elif [[ "$DJANGO_PORT" != "" ]]; then
    echo Setting port to DJANGO_PORT "$DJANGO_PORT"
    port="$DJANGO_PORT"
else
    echo Setting port to 8000
    port=8000
fi
echo Port is "$port"

echo
echo --- Executing python manage.py makemigrations ---
echo
python manage.py makemigrations || {
    echo "ERROR: python manage.py makemigrations failed"
    return 1
}


echo
echo --- Executing python manage.py migrate ---
echo
python manage.py migrate || {
    echo "ERROR: python manage.py migrate failed"
    return 1
}

echo
echo --- Executing python manage.py shell to check if "$DJANGO_SUPERUSER_USERNAME" exists
echo
python manage.py shell -c "from core.models import User; exists = (User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists()); sys.exit(0 if exists else 1)"

superuser_exists=$?

if [ $superuser_exists -eq 1 ]; then
  echo
  echo --- Executing python manage.py createsuperuser ---
  echo
  if ! python manage.py createsuperuser --username "$DJANGO_SUPERUSER_USERNAME" --email "$DJANGO_SUPERUSER_EMAIL" --no-input;
  then
    echo "ERROR: python manage.py createsuperuser failed"
    return 1
  fi
else
  echo --- INFO: Skipping python manage.py createsuperuser - super user "$DJANGO_SUPERUSER_USERNAME" already exists.
fi

echo
echo --- All prep steps successful!  Executing python manage.py runserver on "$port"
echo

python manage.py runserver "$port"
