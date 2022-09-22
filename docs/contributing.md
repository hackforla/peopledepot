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

1. [Temporary] The latest code is in https://github.com/fyliu/peopledepot.git and we need to get that.

   1. Create a git remote `fang` to that repo

       ```bash
       git remote add fang https://github.com/fyliu/peopledepot.git
       ```

   1. Fetch data from the remote

       ```bash
       git fetch fang
       ```

   1. Checkout the recurring_event-model branch to see the current progress. The main repo should be updated with the latest code soon.

       ```bash
       git checkout fang/recurring_event-model-PR
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

1. Run all tests

    ```bash
    ./scripts/test.sh
    ```

### Linting and autoformatting

We're using the popular [flake8][flake8-docs] and [black][black-docs] for linting and code formatting. We're also using [isort][isort-docs] to organize import statements.

To run them, use the `lint.sh` convenience script or look inside the script to see how to run them individually.

1. Run `lint.sh`

    ```bash
    ./scripts/lint.sh
    ```

### Pre-commit checks

We will eventually integrate this into pre-commit hooks, but for now, run this command before each git commit

1. Run `precommit-check.sh`

    ```bash
    ./scripts/precommit-check.sh
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

#### Submit a bug

#### Submit a feature request

#### Contribute to an existing issue

1. Find issue in Prioritized Backlog [here](https://github.com/hackforla/peopledepot/projects/1)
1. Assign issue to yourself and move it to In progress
1. Follow the steps in the issue description to complete the issue
1. Create a pull request and tag it with the issue number (i.e. closes #15)

To create a new issue, please use the blank issue template (available when you click New Issue).  If you want to create an issue for other projects to use, please create the issue in your own repository and send a slack message to one of your hack night hosts with the link.

### Working with forks and branches

We use the fork, branch, and pull request model

To contribute code changes

1. Choose an issue to work on, say issue #15
1. Create a fork and commit your work inside the fork
   1. Fork the repo from [hackforla/peopledepot](https://github.com/hackforla/peopledepot)
   1. Create a branch in your fork to work on the issue. It's preferred to have the working issue number in the branch name.
   1. Remember to run the `precommit-checks.sh` script before each commit until it can be integrated
1. Create a PR from your fork/branch to hackforla/peopledepot/main when you're done with your changes
   1. Reference the issue that you're working on in the PR description. e.g. "Closes #15"
   1. Provide a description of the relevant changes.
1. Move the issue to the Review column in the project board

### Working with pull requests and reviews

- Explain your process.

[docker-install]: https://docs.docker.com/get-docker/
[docker-compose-install]: https://docs.docker.com/compose/install/
[flake8-docs]: https://github.com/pycqa/flake8
[black-docs]: https://github.com/psf/black
[isort-docs]: https://github.com/pycqa/isort/
