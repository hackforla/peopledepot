#!/bin/bash
if [ "$BASE_DIR" == "" ]; then
    echo "BASE_DIR is not set"
    return 1
fi

cd $BASE_DIR
# Add the base directory to the PYTHONPATH
export PYTHONPATH=$BASE_DIR:$PYTHONPATH
python manage.py load_command
