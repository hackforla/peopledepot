#!/bin/bash
set -euo pipefail
IFS=$'\n\t'
set -x

# Default options
COVERAGE="--no-cov"
CHECK_MIGRATIONS=true
N_CPU="auto"
PYTEST_ARGS=()  # Initialize as an empty array

# Function to display help
show_help() {
  cat << EOF
Usage: ${0##*/} [OPTIONS] [pytest-args]

Options:
  --coverage         Run tests with coverage (default: without coverage, using --no-cov).
  --skip-migrations  Skip checking for pending migrations before running tests (default: check migrations).
  -n                 Remove the default --n=auto option for running tests (default: --n=auto).
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
  echo "Debug: $arg"
  case $arg in
    --help)
      show_help
      exit 0
      ;;
    --help-pytest)
      pytest --help
      exit 0
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
      echo "Number of CPUs set to: $N_CPU"
      ;;
    *)
      PYTEST_ARGS+=("$arg")  # Preserve other arguments for pytest
      echo "Adding ${PYTEST_ARGS[*]} to pytest"
      ;;
  esac
  shift # Shift to the next argument
done

# If no additional args are passed, use an empty string
if [ ${#PYTEST_ARGS[@]} -eq 0 ]; then
  PYTEST_ARGS=("")
  echo "No positional arguments were passed, defaulting to an empty string."
else
  echo "Final PYTEST_ARGS: ${PYTHON_ARGS[*]}"
fi

# Check for missing migration files if not skipped
if [ "$CHECK_MIGRATIONS" = true ]; then
  echo "Checking for missing migrations..."
  docker-compose exec -T web python manage.py makemigrations --check
fi

# Run pytest with the parsed arguments
echo "Running: docker-compose exec -T web pytest -n $N_CPU $COVERAGE ${PYTEST_ARGS[*]}"
docker-compose exec -T web pytest -n "$N_CPU" $COVERAGE "${PYTEST_ARGS[*]}"
