# Convenience Scripts

These are designed to make it easier to perform various everyday tasks in the project. They try to be transparent by exposing the underlying commands they execute so that users can have an idea of what's happening and try to learn the commands if they wish.

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

    1. This assumes that `DJANGO_SUPERUSER_USERNAME` and `DJANGO_SUPERUSER_PASSWORD` are set in `.env.dev`

1. **db.sh** - connect to the database in the `db` container

    1. This is a different route than `manage.py dbshell`, which requires the `psql` executable in the `web` container

1. **erd.sh** - generate ER diagram

    - The image is saved to `app/erd.png`
    - This script is dependent on the `graphviz` package

1. **lint.sh** - lint and and auto-format code

1. **loadenv.sh** - load environment variables from `.env.dev` into shell environment

1. **logs.sh** - view/tail container logs

1. **migrate.sh** - run database migrations inside container

    1. Add `<app> <migration_number>` to migrate to that database state. Ex: `migrate.sh core 0010`

1. **precommit-check.sh** - sanity checks before committing code

    1. Call `buildrun.sh`, `lint.sh`, and `test.sh`

1. **run.sh** - start the development server in Docker, with some options

    1. Pass in `-h` to show usage

1. **start-local.sh** - start the development server natively

1. **test.sh** - run tests and generate test coverage report

    1. Use the `-k` flag to filter tests. For example `test.sh -k program_area` will select only tests with "program_area" in the name.
    1. Pass in `--no-cov` to disable the coverage report. The coverage report will show many missing lines of coverage as a result.

1. **update-dependencies.sh** - update python dependencies to the latest versions
