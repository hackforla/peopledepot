# Contributing to PeopleDepot

## Quick start

1. Install or make sure [docker][docker-install] and [docker-compose][docker-compose-install] are installed on your computer

```bash
    docker -v
    docker-compose -v
```

1. Clone this repo and change to the project root directory

```bash
    git clone https://github.com/hackforla/peopledepot.git
    cd peopledepot
```

1. Create .env.dev from .env.dev-sample

```bash
    cp .env.dev-sample .env.dev
```

1. Build and run via the script

```bash
    ./scripts/buildrun.sh
```

1. Create a super user for logging into the web admin interface

```bash
    docker-compose exec web python manage.py createsuperuser
```

1. Browse to the web admin interface at `http://localhost:8000/admin/`

### Testing

1. Make sure containers are running

```bash
    docker-compose up -d
```

1. Run all tests

```bash
    ./scripts/test.sh
```

### Linting and autoformatting

We're using the popular [flake8][flake8-docs] and [black][black-docs] for linting and code formatting. We're also using [isort][isort-docs] to organize import statements.

To run them, use the `lint.sh` convenience script or look inside the script to see how to run them individually.

1. Make sure containers are running

```bash
    docker-compose up -d
```

1. Run `lint.sh`

```bash
    ./scripts/lint.sh
```

### Convenience scripts for sanity checks before committing code (assumes bash env)

1. buildrun.sh - clean, build, and run containers in background mode
1. lint.sh - lint and and auto-format code
1. test.sh - run tests and generate test coverage report
1. logs.sh - view container logs
1. migrate.sh - run database migrations inside container
1. precommit-check.sh - sanity checks before committing (calls other scripts, but doesn't stop progress on error like it should)
1. createsuperuser.sh - creates a default superuser (assumes apt env. requires `expect` util to be installed)

### Working with issues

- Explain how to submit a bug.
- Explain how to submit a feature request.
- Explain how to contribute to an existing issue.

To create a new issue, please use the blank issue template (available when you click New Issue).  If you want to create an issue for other projects to use, please create the issue in your own repository and send a slack message to one of your hack night hosts with the link.

### Working with forks and branches

- Explain your guidelines here.

### Working with pull requests and reviews

- Explain your process.

[docker-install]: https://docs.docker.com/get-docker/
[docker-compose-install]: https://docs.docker.com/compose/install/
