#!/bin/bash
# return 0 will succeed if sourced, fail if not sourced
# 2>/dev/null will suppress the error message
(return 0 2>/dev/null) && sourced="true" || sourced="false"
if [ "$sourced" != "true" ]; then
    echo "Error, script not sourced.  Please run 'source ./activate.sh'"
    exit 1
fi

source ./venv/bin/activate
# next comment is to ignore flake8 error for the following line when pre-commit runs
# flake8: noqa
if [[ "$?" == 0 ]]; then
  echo "Sourced OK (called from ${BASH_SOURCE[1]})"
else
  echo "ERROR: activation failed (called from ${BASH_SOURCE[1]})"
fi
echo Done
