#!/bin/bash
# return 0 will succeed if sourced, fail if not sourced
# 2>/dev/null will suppress the error message
(return 0 2>/dev/null) && sourced="true" || sourced="false"
VENV_NAME=venv
if [ "$sourced" != "true" ]; then
    echo "Error, script not sourced.  Please run 'source ./activate.sh'"
    (return 1)
fi
# shellcheck disable=SC1091
source $VENV_NAME/bin/activate || echo "Error, $VENV_NAME/bin/activate not found.  Please run 'python3 -m venv $VENV_NAME' to create it." && (return 1)
# shellcheck disable=SC2181
if [[ "$?" == 0 ]]; then
  echo "Sourced OK (called from ${BASH_SOURCE[1]})"
else
  echo "ERROR: activation failed (called from ${BASH_SOURCE[1]})"
fi
echo Done
