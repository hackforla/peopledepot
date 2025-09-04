# Convenience Scripts

These are designed to make it easier to perform various everyday tasks in the project. They try to be transparent by exposing the underlying commands they execute so that users can have an idea of what's happening and try to learn the commands if they wish.

## Scripts

```bash
scripts/
├── buildrun.sh
├── check-migrations.sh
├── createsuperuser.sh
├── db.sh
├── erd.sh
├── lint.sh
├── loadenv.sh
├── logs.sh
├── migrate.sh
├── precommit-check.sh
├── run.sh
├── start-local.sh
├── test.sh
└── update-dependencies.sh
```

These scripts assume you are using bash.

1. **buildrun.sh** - clean, build, and run containers in background mode

    1. Pass in `-v` to remove data volume, which resets the local database.
    1. See the script file for more options.

1. **check-migrations.sh** - check if migrations are up to date

1. **createsuperuser.sh** - create a default superuser

    1. This assumes that `DJANGO_SUPERUSER_USERNAME` and `DJANGO_SUPERUSER_PASSWORD` are set in `.env.docker`

1. **db.sh** - connect to the database in the `db` container

    1. This is a different route than `manage.py dbshell`, which requires the `psql` executable in the `web` container

1. **erd.sh** - generate ER diagram

    - The image is saved to `app/erd.png`
    - This script is dependent on the `graphviz` package

1. **lint.sh** - lint and and auto-format code

1. **logs.sh** - view/tail container logs

1. **migrate.sh** - run database migrations inside container

    1. Add `<app> <migration_number>` to migrate to that database state. Ex: `migrate.sh core 0010`

1. **precommit-check.sh** - sanity checks before committing code

    1. Call `buildrun.sh`, `lint.sh`, and `test.sh`

1. **run.sh** - start the development server in Docker, with some options

    1. Pass in `-h` to show usage

1. **shell.sh** - open a shell on the terminal

    1. Pass in `-h` to show usage

1. **test.sh** - run tests and generate test coverage report

    1. Use the `-k` flag to filter tests. For example `test.sh -k program_area` will select only tests with "program_area" in the name.
    1. use `--help` to see other script options.
    1. use `--help-pytest` to see pytest options that can be added.

1. **update-dependencies.sh** - update python dependencies to the latest versions

## Script Elements

### Header

```bash
#!/bin/bash
set -euo pipefail
# IFS=$'\n\t'
```

1. `set -euo pipefail` is a combination of the following
    1. `set -e` exits the script immediately if a command fails
    1. `set -u` exits the script if an undefined variable is used
    1. `set -o pipefail` exits the script if a pipe command fails
1. `IFS=$'\n\t'` sets the internal field separator to newlines and tabs

Why do we use this?

- This was the header to set up what's known as the [unofficial bash strict mode](http://redsymbol.net/articles/unofficial-bash-strict-mode/), which is supposed to help people write better bash scripts.
- Some of it is outdated like the reasoning to use `IFS=$'\n\t'` is solved by the `shellcheck` tool.
    - There are posts warning of `set -e` [not being safe in some cases](https://gist.github.com/mohanpedala/1e2ff5661761d3abd0385e8223e16425?permalink_comment_id=4661118#gistcomment-4661118).
    - The `IFS` setting may [not be needed](https://gist.github.com/mohanpedala/1e2ff5661761d3abd0385e8223e16425?permalink_comment_id=4661118#gistcomment-4661118) since we use shellcheck to make sure variables are quoted properly.
    - [More link](https://gist.github.com/mohanpedala/1e2ff5661761d3abd0385e8223e16425)

### Debugging

We use `set -x` pairs to enable debug mode, which prints the commands that are executed in between them. The idea is to expose the underlying commands so we can learn them if we want to.

```bash
set -x
docker-compose exec -T web python manage.py makemigrations --check
{ set +x; } 2>&-;
```

1. `set -x` enables debug mode
1. `set +x` disables debug mode. Use `{ set +x; } 2>&-;` to hide the `set +x` from echoing to the terminal. It executes in a subshell to disable debug mode and redirects stderr to `/dev/null`
1. The disable command is not necessary if the script ends right away.

### SCRIPT_DIR

We use `SCRIPT_DIR="$(dirname "$0")"` to get the directory of the script file, which is useful for calling other scripts in the same directory.

```bash
"$SCRIPT_DIR"/buildrun.sh
```

### Extra arguments

1. `"$@"` contains all the arguments to the script

    ```bash
    "$SCRIPT_DIR"/run.sh -c -o -d -b -m "$@"
    ```

1. `"$1"` is the first argument

    ```bash
    csv_file=$1
    ```

1. For example of reading commandline options, see `run.sh` and `test.sh`.
