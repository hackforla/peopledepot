#!/bin/bash
set -euo pipefail
IFS=$'\n\t'
set -x

SCRIPT_DIR="$(dirname "${BASH_SOURCE[0]}")"
echo SCRIPT_DIR = "$SCRIPT_DIR"
# https://codefather.tech/blog/bash-get-script-directory/

# clean, build, and run in background
# c     Delete docker containers and networks
# v    *Remove docker volumes
# o    *Remove docker orphan containers
# d     Run in background
# b     Rebuild
# m     Run migrations
# s     Create superuser
# l     Tail logs after run
handle_error() {
    echo "An error occurred. Script terminated."
    # Additional error handling code can be added here
}

# Set up trap to catch errors and call the error handling function
trap 'handle_error' ERR

"$SCRIPT_DIR"/run.sh -c -o -d -b -m "$@"
echo "Done"
