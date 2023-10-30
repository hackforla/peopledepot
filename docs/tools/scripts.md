# Convenience Scripts

These are designed to make it easier to perform various everyday tasks in the project. They try to be transparent by exposing the underlying commands they execute so that users can have an idea of what's happening and try to learn the commands if they wish.

These scripts assume you are using bash.

1. **buildrun.sh** - clean, build, and run containers in background mode

    1. Pass in `-v` to remove data volume, which resets the local database.
    1. See the script file for more options.

1. **lint.sh** - lint and and auto-format code

1. **test.sh** - run tests and generate test coverage report

    1. Use the `-k` flag to filter tests. For example `test.sh -k program_area` will select only tests with "program_area" in the name. The coverage report will show many missing lines of coverage as a result. We recommend adding `--no-cov` in this case to disable the coverage report.

1. **logs.sh** - view/tail container logs

1. **migrate.sh** - run database migrations inside container

    1. Add `<app> <migration_number>` to migrate to that database state. Ex: `migrate.sh core 0010`

1. **precommit-check.sh** - sanity checks before committing code

1. **createsuperuser.sh** - creates a default superuser.

    1. This assumes that `DJANGO_SUPERUSER_USERNAME` and `DJANGO_SUPERUSER_PASSWORD` are set in `.env.dev`
