#!/bin/bash

# Note about -e: Intentionally not "set -e..." so that if there is a syntax error,
# the shell will not close.  Unless you are joining commands with ||
#
# set -o pipefail will catch any failing command unless commands joined by ||
# -u : errors if variable is not set
# -o pipefail : script terminates if any command fails
echo starting

# Handle errors gracefully without exiting the shell session.


# Main function to contain the logic.
main() {

  echo In main
  if [[ "${BASH_SOURCE[0]}" != "${0}" ]]; then
    echo "The script was sourced."
  else
    echo "Error: the script must be sourced."
    return 1
  fi
  ORIGINAL_DIR=$PWD

  if [ -f "path.sh" ]; then
    echo path.sh is in current directory
  elif [ -f "../scripts/path.sh" ]; then
    echo "cd ../scripts"
    cd ../scripts || return 1
  elif [ -f "scripts/path.sh" ]; then
    echo "cd scripts"
    cd scripts || return 1
  elif [ ! -f "path.sh" ]; then
    echo "Could not find path.sh relative to the current directory."
    return 1
  fi

  echo Checking path

  if [[ "$PATH" = *"$PWD"* ]]; then
    echo Path is already set
  else
    echo "Adding $PWD to PATH"
    export PATH="$PATH:$PWD"
  fi

  echo "cd $ORIGINAL_DIR"
  cd $ORIGINAL_DIR || return 1

  echo "Script completed successfully."
}

# Run the main function.
main
