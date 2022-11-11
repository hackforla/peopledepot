# How to Contribute to PeopleDepot

## Setting up the development environment

### **1.2 Dev setup (2): Installing Git**

Before cloning your forked repository to your local machine, you must have Git installed. You can find instructions for installing Git for your operating system [**here**](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git). Please note that if you have a Mac the page offers several options (see other option, if you need to conserve hard drive space) including:

- an “easiest” option (this version is fine for use at hackforla): This option would take just over 4GB.
- a “more up to date” option (not required but optional if you want it): This option prompts you to go to install an 8GB package manager called Homebrew. 
- Other option: If your computer is low on space, you can use this [tutorial](https://www.datacamp.com/community/tutorials/homebrew-install-use) to install XCode Command Tools and a lighter version of Homebrew and then install Git using this command: ```$ brew install git```  which in total only uses 300MB.

### **1.3 Dev setup (3): Fork the repository**

You can fork the hackforla/peopledepot repository by clicking <a href="https://github.com/hackforla/peopledepot/fork"> <button> <img src="https://user-images.githubusercontent.com/17777237/54873012-40fa5b00-4dd6-11e9-98e0-cc436426c720.png" width="8px"> Fork</button></a>
. A fork is a copy of the repository that will be placed on your GitHub account.

**Note:** It should create a URL that looks like the following -> `https://github.com/<your_GitHub_user_name>/peopledepot`.

**For example** -> `https://github.com/octocat/peopledepot`.

**Be Aware:** What you have created is a forked copy in a remote version on GitHub. It is not yet on your local machine yet.

### **1.4 Dev setup (4): Clone (Create) a copy on your computer**

Before creating a copy to your local machine, you must have Git installed. You can find instructions for installing Git for your operating system [**here**](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git). 

The following steps will clone (create) a local copy of the forked repository on your computer.

#### **1.4.a Clone repo (1): Create  `hackforla` folder**

Create a new folder in your computer that will contain `hackforla` projects.

In your command line interface (Terminal, Git Bash, Powershell), move to where you want your new folder to be placed and create a new folder in your computer that will contain `hackforla` projects. After that, navigate into the folder(directory) you just created.
      
For example: 
```bash
mkdir hackforla
cd hackforla
```
      
and run the following commands:
      
```bash
git clone https://github.com/<your_GitHub_user_name>/peopledepot.git
```
      
For example if your GitHub username was `octocat`:
```bash
git clone https://github.com/octocat/peopledepot.git
```

You should now have a new folder in your `hackforla` folder called `peopledepot`. Verify this by changing into the new directory:

```bash
cd peopledepot
```

### **1.5 Dev setup (5): Set up Docker**
Install or make sure [docker][docker-install] and [docker-compose][docker-compose-install] are installed on your computer

    ```bash
    docker -v
    docker-compose -v
    ```

The recommended installation method for your operating system can be found [here](https://docs.docker.com/install/). <strong><em>Feel free to reach out in the [Hack for LA Slack channel](https://hackforla.slack.com/messages/people-depot/) if you have trouble installing docker on your system</em></strong>

More on using Docker and the concepts of containerization:

* [Get started with Docker](https://docs.docker.com/get-started/)

#### **1.5.a Docker installation troubleshooting**

If you are on Windows and get 'You are not allowed to use Docker, you must be in the "docker-users" group' as an error message, the following wiki page is a guide for solving te issue:
- [Windows docker-users group error guide](https://github.com/hackforla/website/wiki/Adding-local-user-accounts-to-the-docker-users-group-on-Windows-10)

Installing WSL2 on windows
- https://docs.microsoft.com/en-us/windows/wsl/install-win10

### **1.6 Dev setup (6): Build and run the project locally with the script**

**IMPORTANT:** Please make sure the `Docker Desktop` application is **running on your computer** before you run the bash commands below.

1. Create an .env.dev file from .env.dev-sample

    ```bash
    cp .env.dev-sample .env.dev
    ```

2. Build and run the project via the script

    ```bash
    ./scripts/buildrun.sh
    ```

2. Create a super user for logging into the web admin interface

    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

3. Browse to the web admin interface at `http://localhost:8000/admin/` and confirm the admin site is running. Use the credentials you created in Step 2 (above) to log in.

#### **1.6.a Stopping Docker**

To stop the service-container, but not destroy it (often sufficient for day-to-day work):

```bash
docker-compose stop
```

To stop and destroy the service container:
```bash
docker-compose down
```

Add the `-v` flag to destroy the data volumes as well:
```bash
docker-compose down -v
```

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


