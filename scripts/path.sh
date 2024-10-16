#!/bin/bash

 Check if the script was sourced
if [[ "${BASH_SOURCE[0]}" != "${0}" ]]; then
    echo "Script was sourced."
else
    echo "Script was not sourced. Exiting with status 1."
    exitrm 1
fi

CURRENT_PATH=$PWD
cd scripts || cd app/scripts || cd ../scripts || echo Unable to set path & return 1
export PATH=$PATH:$PWD
cd $CURRENT_PATH


