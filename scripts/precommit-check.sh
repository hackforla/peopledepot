#!/bin/bash
set +x

SCRIPT_DIR="$(dirname "${BASH_SOURCE[0]}")"

"$SCRIPT_DIR"/lint.sh &&
"$SCRIPT_DIR"/buildrun.sh &&
"$SCRIPT_DIR"/test.sh
