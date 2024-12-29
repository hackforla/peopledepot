#!/bin/bash
set -euo pipefail
IFS=$'\n\t'
# Default options
COVERAGE="--no-cov"
EXEC_COMMAND=true
CHECK_MIGRATIONS=true
N_CPU="auto"
PYTEST_ARGS=("")

# Function to display help
show_help() {
  cat << EOF
Usage: ${0##*/} [OPTIONS] [pytest-args]

Options:
  --coverage         Run tests with coverage (default: without coverage, using --no-cov).
  --skip-migrations  Skip checking for pending migrations before running tests (default: check migrations).
  -n                 Remove the default --nauto option for running tests (default: -n auto).  There must be
                       a space after -n and the value.  (If you use 1 the script changes the value to 0.)
  --help             Display this help message and exit.
  --help-pytest      Display pytest help.

Other parameters passed to the script will be forwarded to pytest as specified.

By default:
  - Tests run without coverage.
  - Migrations are checked before running tests.
  - Tests are run using --n auto for optimal parallel execution.
EOF
}

# Parse arguments
while [[ $# -gt 0 ]]; do
  arg="$1" # Use $1 as the current argument
  case $arg in
    --help)
      show_help
      exit 0
      ;;
    --help-pytest)
      pytest --help
      exit 0
      ;;
    --no-exec)
      EXEC_COMMAND=false
      ;;
    --coverage)
      COVERAGE=""  # Enable coverage
      echo "Coverage enabled"
      ;;
    --skip-migrations)
      CHECK_MIGRATIONS=false  # Skip migration checks
      echo "Skipping migration checks"
      ;;
    -n)
      shift
      N_CPU="$1"
      if [ "$N_CPU" == "1" ]; then
        N_CPU=0
      fi
      ;;
    *)
      PYTEST_ARGS+=("$arg")  # Preserve other arguments for pytest
      echo "Positional argument added: $arg"
      echo "Current python args: ${PYTEST_ARGS[*]}"
      ;;
  esac
  shift # Shift to the next argument
done

# Check for missing migration files if not skipped
if [ "$CHECK_MIGRATIONS" = true ]; then
  echo "Checking for missing migrations..."
  set -x
  docker-compose exec -T web python manage.py makemigrations --check
  set +x
fi

if [ "$EXEC_COMMAND" = true ]; then
  set -x
  docker-compose exec -T web pytest -n "$N_CPU" $COVERAGE "${PYTEST_ARGS[@]}"
  set +x
else
  echo docker-compose exec -T web pytest -n "$N_CPU" $COVERAGE "${PYTEST_ARGS[@]}"
fi
