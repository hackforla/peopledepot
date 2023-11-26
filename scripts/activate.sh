# return 0 will succeed if sourced, fail if not sourced
# 2>/dev/null will suppress the error message
(return 0 2>/dev/null) && sourced="true" || sourced="false"
VENV_NAME=$(basename $PWD)-venv
if [ "$sourced" != "true" ]; then
    echo "Error, script not sourced.  Please run 'source ./activate.sh'"
    exit 1
fi
source $VENV_NAME/bin/activate
if [[ "$?" == 0 ]]; then
  echo "Sourced OK (called from ${BASH_SOURCE[1]})"
else
  echo "ERROR: activation failed (called from ${BASH_SOURCE[1]})"
fi
echo Done

