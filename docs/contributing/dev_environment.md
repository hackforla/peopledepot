# Setting Up Development Environment

## Pre-requisites

### GitHub account

See [here](https://docs.github.com/en/get-started/signing-up-for-github/signing-up-for-a-new-github-account#signing-up-for-a-new-account) for creating a GitHub account. If you are not familiar with Git, [this tutorial](https://docs.github.com/en/get-started/quickstart/hello-world) is recommended.

### Two-factor authentication

Set up two-factor authentication on your account by following this [guide](https://docs.github.com/en/github/authenticating-to-github/configuring-two-factor-authentication).

### Text editor

[VS Code](https://code.visualstudio.com/download) is recommended, but feel free to use a text editor of your choice.

### Install Git

Before cloning your forked repository to your local machine, you must have Git installed. You can find instructions for installing Git for your operating system [**here**](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

=== "Windows"
    - we recommend [installing Windows Subsystem for Linux (WSL)](https://code.visualstudio.com/docs/remote/wsl). WSL provides a Linux-compatible environment that can prevent common errors during script execution.

    - After setting up WSL, install Git directly from the Linux terminal. This method can help avoid complications that sometimes arise when using Git Bash on Windows.

    - If you prefer Git Bash or encounter errors related to line endings when running scripts, the problem might be due to file conversions in Windows. To address this, configure Git as follows:

        ```bash
        git config --system set autocrlf=false
        ```

        !!! tip "Feel free to reach out in the [Hack for LA Slack channel](https://hackforla.slack.com/messages/people-depot/) if you encounter any errors while running scripts on Windows"

=== "Mac"
    Please note that if you have a Mac the page offers several options (see other option, if you need to conserve hard drive space) including:

    - an “easiest” option (this version is fine for our use): This option would take just over 4GB.
    - a “more up to date” option (not required but optional if you want it): This option prompts you to go to install an 8GB package manager called Homebrew.
    - Other option: If your computer is low on space, you can use this [tutorial](https://www.datacamp.com/community/tutorials/homebrew-install-use) to install XCode Command Tools and a lighter version of Homebrew and then install Git using this command: `$ brew install git` which in total only uses 300MB.

### Install Docker

Install or make sure [docker][docker-install] and [docker-compose][docker-compose-install] are installed on your computer

```bash
docker -v
docker-compose -v
```

The recommended installation method for your operating system can be found [here](https://docs.docker.com/install/).

!!! tip "Feel free to reach out in the [Hack for LA Slack channel](https://hackforla.slack.com/messages/people-depot/) if you have trouble installing docker on your system"

More on using Docker and the concepts of containerization:

- [Get started with Docker](https://docs.docker.com/get-started/)

## Fork the repository

You can fork the hackforla/peopledepot repository by clicking <a href="https://github.com/hackforla/peopledepot/fork"> <button> <img src="https://user-images.githubusercontent.com/17777237/54873012-40fa5b00-4dd6-11e9-98e0-cc436426c720.png" width="8px"> Fork</button></a>
. A fork is a copy of the repository that will be placed on your GitHub account.

!!! note "It should create a URL that looks like the following -> `https://github.com/<your_GitHub_user_name>/peopledepot`"
    !!! example "For example -> `https://github.com/octocat/peopledepot`"

!!! info "What you have created is a forked copy in a remote version on GitHub. It is not on your local machine yet"

### Clone a copy on your computer

The following steps will clone (create) a local copy of the forked repository on your computer.

1. Create a new folder in your computer that will contain `hackforla` projects.

    In your command line interface (Terminal, Git Bash, Powershell), move to where you want your new folder to be placed and create a new folder in your computer that will contain `hackforla` projects. After that, navigate into the folder(directory) you just created.

    For example:

    ```bash
    cd /projects
    mkdir hackforla
    cd hackforla
    ```

1. From the hackforla directory created in previous section:

    ```bash
    git clone https://github.com/<your_GitHub_user_name>/peopledepot.git
    ```

    For example if your GitHub username was `octocat`:

    ```bash
    git clone https://github.com/octocat/peopledepot.git
    ```

    !!! note "You can also clone using ssh which is more secure but requires more setup. Because of the additional setup, cloning using https as shown above is recommended"

You should now have a new folder in your `hackforla` folder called `peopledepot`. Verify this by changing into the new directory:

```bash
cd peopledepot
```

### Verify and set up remote references

Verify that your local cloned repository is pointing to the correct `origin` URL (that is, the forked repo on your own GitHub account):

```bash
git remote -v
```

You should see `fetch` and `push` URLs with links to your forked repository under your account (i.e. `https://github.com/<your_GitHub_user_name>/peopledepot.git`). You are all set to make working changes to the project on your local machine.

However, we still need a way to keep our local repo up to date with the deployed project. To do so, you must add an upstream remote to incorporate changes made while you are working on your local repo. Run the following to add an upstream remote URL & update your local repo with recent changes to the `hackforla` version:

```bash
git remote add upstream https://github.com/hackforla/peopledepot.git
git fetch upstream
```

After adding the upstream remote, you should now see it if you again run `git remote -v` :

```bash
origin  https://github.com/<your_GitHub_user_name>/peopledepot.git (fetch)
origin  https://github.com/<your_GitHub_user_name>/peopledepot.git (push)
upstream        https://github.com/hackforla/peopledepot.git (fetch)
upstream        https://github.com/hackforla/peopledepot.git (push)
```

## Build and run using Docker locally

1. Make sure the Docker service is running

    === "Docker (Engine)"
        ```bash
        sudo systemctl status docker
        ```

        It will show `Active: active (running)` if it's running.

    === "Docker Desktop"
        1. Start Docker Desktop
        1. Run `docker container ls` to verify Docker Desktop is running. If it is not running you will get the message: `Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?`

1. Create an .env.docker file from .env.docker-example

    ```bash
    cp ./app/.env.docker-example ./app/.env.docker
    ```

1. Build and run the project via the script (this includes running `docker-compose up`)

    ```bash
    ./scripts/buildrun.sh
    ```

1. Create a super user for logging into the web admin interface

    ```bash
    docker-compose exec web python manage.py createsuperuser --no-input
    ```

1. Browse to the web admin interface at `http://localhost:8000/admin/` and confirm the admin site is running. Use DJANGO_SUPERUSER_USERNAME and DJANGO_SUPERUSER_PASSWORD from .env.docker for credentials.

## Install pre-commit

This will check your changes for common problems.

See the [Pre-commit page](tools/pre-commit.md) for installation instructions.

For consistency, an automated bot will perform the same checks on the repository side when you open a pull request.

[docker-compose-install]: https://docs.docker.com/compose/install/
[docker-install]: https://docs.docker.com/get-docker/
