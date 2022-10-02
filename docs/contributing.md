# Contributing to PeopleDepot

## Quick start

1. Install or make sure [docker][docker-install] and [docker-compose][docker-compose-install] are installed on your computer

    - It's best to use the `docker-compose` installation instructions which also installs docker.

    ```bash
    docker -v
    docker-compose -v
    docker ps
    ```
    1. `docker ps` should print a list of docker containers. Even a blank list signals that the docker daemon (service) is running.

1. Fork the PeopleDepot repo from Github

   1. The Fork button is near the upper-right of the screen

1. Clone your forked repo and change to the project root directory

    ```bash
    git clone https://github.com/[username]/peopledepot.git
    cd peopledepot
    ```

1. Add the HackforLA repo as the `hackforla` remote and fetch from it

   ```bash
    git remote add hackforla https://github.com/hackforla/peopledepot.git
    git fetch hackforla
    ```

    1. When you push your code later, you should specify the remote to push to. i.e. `git push origin`, where `origin` is the default remote that points to your fork when you first cloned it to your local machine

1. [Temporary] The latest code is in https://github.com/fyliu/peopledepot.git and we need to get that.

   1. Create a git remote `fang` to that repo

       ```bash
       git remote add fang https://github.com/fyliu/peopledepot.git
       ```

   1. Fetch data from all the remotes, including from `fang`

       ```bash
       git fetch --all
       ```

   1. Checkout the development branch to see the current progress. The main repo should be updated with the latest code soon.

       ```bash
       git checkout fang/development
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

1. Run all tests from the project root

    ```bash
    ./scripts/test.sh
    ```

### Linting and autoformatting

We're using the popular [flake8][flake8-docs] and [black][black-docs] for linting and code formatting. We're also using [isort][isort-docs] to organize import statements.

To run them, use the `lint.sh` convenience script or look inside the script to see how to run them individually.

1. Run the lint script from the project root

    ```bash
    ./scripts/lint.sh
    ```

### ~~Pre-commit checks~~ (Replaced by the pre-commit hooks below. DELETE AFTER THE TEAM IS OK WITH THE HOOKS)

We will eventually integrate this into pre-commit hooks, but for now, run this command before each git commit

1. Run `precommit-check.sh`

    ```bash
    ./scripts/precommit-check.sh
    ```

### Pre-commit hooks

The pre-commit hook in git will run before each commit and will abort the commit on failure. The advantage of this over github actions is that github actions work on code that's already committed, so it needs to allow code to be committed first.

We're setting a set of fast checks to run on each commit and longer checks such as a full rebuild to run when trying to push the code.

The hooks run when doing normal `git commit` and `git push` commands. It's recommended to do this in the command line. If performing these actions from a gui application, the interface may seem to hang for some time.

Installing the pre-commit hooks to git

1. Install pre-commit (virtual environment or at least per-user install is recommended)

   ```bash
   pip install pre-commit --local
   ```

1. Add the hook to git

   ```bash
   pre-commit install
   ```

1. Update pre-commit and plugins to the latest version

   ```bash
   pre-commit autoupdate
   ```

1. Test run the hooks (this runs it against all files rather than only staged files)

   ```bash
   pre-commit run --all-files
   ```

1. (Extra info) More commands to test run the hooks

    ```bash
    pre-commit run --all-files --hook-stage push
    pre-commit run --all-files --hook-stage commit
    pre-commit run test --all-files --hook-stage push
    ```

### Convenience scripts for sanity checks before committing code (assumes bash env)

1. buildrun.sh - clean, build, and run containers in background mode
1. lint.sh - lint and and auto-format code
1. test.sh - run tests and generate test coverage report
1. logs.sh - view/tail container logs
1. migrate.sh - run database migrations inside container
1. precommit-check.sh - sanity checks before committing code
1. createsuperuser.sh - creates a default superuser (assumes debian env.)

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
