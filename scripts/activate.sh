#!/bin/bash
# return 0 will succeed if sourced, fail if not sourced
# 2>/dev/null will suppress the error message
(return 0 2>/dev/null) && sourced="true" || sourced="false"
if [ "$sourced" != "true" ]; then
    echo "Error, script not sourced.  Please run 'source ./activate.sh'"
    exit 1
fi

# next comment is to ignore shellcheck error for the following line when pre-commit runs
# shellcheck disable=SC1091
source ./venv/bin/activate

# if previous command completed successfully echo success message, else echo failure message
if true; then
  echo "Sourced OK (called from ${BASH_SOURCE[1]})"
else
  echo "ERROR: activation failed (called from ${BASH_SOURCE[1]})"
fi
echo Done
