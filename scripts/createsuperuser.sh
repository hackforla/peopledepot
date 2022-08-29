#!/bin/bash

# create a test superuser for loggin into django admin
# http://localhost:8000/admin/login

run_install()
{
    ## Prompt the user
    read -p "Do you want to install missing libraries? [Y/n]: " -r answer
    ## Set the default value if no answer was given
    answer="${answer:-Y}"
    ## If the answer matches y or Y, install
    [[ $answer =~ [Yy] ]] && sudo apt-get install "${reqd_pkgs[@]}"
}

reqd_pkgs=("expect")
## Run the run_install function if any of the libraries are missing
set -x
dpkg -s "${reqd_pkgs[@]}" >/dev/null 2>&1 || run_install

/usr/bin/expect << EOF

spawn docker-compose exec web python manage.py createsuperuser --username testadmin --email testadmin@email.com

expect "Password:"
send "Dogfood1!\r"

expect "Password (again): "
send -- "Dogfood1!\r"

expect eof

EOF
