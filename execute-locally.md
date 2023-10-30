Following lines were commented out in .env, used by DOCKER
# SQL_ENGINE=django.db.backends.postgresql
# SQL_DATABASE=people_depot_dev
# SQL_USER=people_depot
# SQL_PASSWORD=people_depot

SQL_PORT changed to 5333 to avoid conflicts, but easier is to not have docker up.  Had to open POSTGRES and change port

From terminal: 
```
export DJANGO_SETTINGS_MODULE=peopledepot.local-settings`
python manage.py runserver
```

