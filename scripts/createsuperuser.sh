#!/bin/bash
set -x

# create a test superuser for loggin into django admin
# http://localhost:8000/admin/login

/usr/bin/expect << EOF

spawn docker-compose exec web python manage.py createsuperuser --username testadmin --email testadmin@email.com

expect "Password:"
send "Dogfood1!\r"

expect "Password (again): "
send -- "Dogfood1!\r"

expect eof

EOF
