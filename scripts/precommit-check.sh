#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

SCRIPT_DIR="$(dirname "${BASH_SOURCE[0]}")"

set -x
"$SCRIPT_DIR"/lint.sh
"$SCRIPT_DIR"/buildrun.sh
"$SCRIPT_DIR"/test.sh
