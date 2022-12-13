Thank you for volunteering your time! The following is a set of guidelines for contributing to the peopledepot repository, which is hosted on GitHub.

**Please make sure you have completed the onboarding process which includes joining the Hack for LA Slack, GitHub, and Google Drive. If you have not been onboarded, see the [Getting Started Page](https://www.hackforla.org/getting-started).** _Workshop attendees are granted a temporary exception from this requirement._

# Join the Repository Team and Google Docs

This step is optional if this is your first time fixing an issue and you want to try fixing an issue without this step.

In the `hfla-site` Slack channel, send an introductory message with your GitHub handle/username asking to be added to the Hack for LA peopledepot GitHub repository, have access to the Google Docs Drive, and Figma.

**NOTE:** Once you have accepted the GitHub invite (comes via email or in your GitHub notifications), **please do the following**:

Make your own Hack for LA GitHub organization membership public by following this [guide](https://help.github.com/en/articles/publicizing-or-hiding-organization-membership#changing-the-visibility-of-your-organization-membership).

# Setting Up the Development Environment

## Pre-requisites

### Github Account

See [here](https://docs.github.com/en/get-started/signing-up-for-github/signing-up-for-a-new-github-account#signing-up-for-a-new-account) for creating a GitHub account. If you are not familiar with Git, [this tutorial](https://docs.github.com/en/get-started/quickstart/hello-world) is recommended.

#### Two Factor Authentication

Set up two-factor authentication on your account by following this [guide](https://docs.github.com/en/github/authenticating-to-github/configuring-two-factor-authentication).

### Text Editor

[VS Code](https://code.visualstudio.com/download) is recommended, but feel free to use a text editor of your choice.

### Install Git

Before cloning your forked repository to your local machine, you must have Git installed. You can find instructions for installing Git for your operating system [**here**](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

For Windows, you may want to [install a Windows Subsystem for Linux (WSL)](https://code.visualstudio.com/docs/remote/wsl) and then install Git from WSL.

Please note that if you have a Mac the page offers several options (see other option, if you need to conserve hard drive space) including:

- an “easiest” option (this version is fine for use at hackforla): This option would take just over 4GB.
- a “more up to date” option (not required but optional if you want it): This option prompts you to go to install an 8GB package manager called Homebrew.
- Other option: If your computer is low on space, you can use this [tutorial](https://www.datacamp.com/community/tutorials/homebrew-install-use) to install XCode Command Tools and a lighter version of Homebrew and then install Git using this command: `$ brew install git` which in total only uses 300MB.

### Install Docker

Install or make sure [docker][docker-install] and [docker-compose][docker-compose-install] are installed on your computer

```bash
    docker -v
    docker-compose -v
```

The recommended installation method for your operating system can be found [here](https://docs.docker.com/install/). <strong><em>Feel free to reach out in the [Hack for LA Slack channel](https://hackforla.slack.com/messages/people-depot/) if you have trouble installing docker on your system</em></strong>

More on using Docker and the concepts of containerization:

- [Get started with Docker](https://docs.docker.com/get-started/)

## Fork the Repository

You can fork the hackforla/peopledepot repository by clicking <a href="https://github.com/hackforla/peopledepot/fork"> <button> <img src="https://user-images.githubusercontent.com/17777237/54873012-40fa5b00-4dd6-11e9-98e0-cc436426c720.png" width="8px"> Fork</button></a>
. A fork is a copy of the repository that will be placed on your GitHub account.

**Note:** It should create a URL that looks like the following -> `https://github.com/<your_GitHub_user_name>/peopledepot`.

**For example** -> `https://github.com/octocat/peopledepot`.

**Be Aware:** What you have created is a forked copy in a remote version on GitHub. It is not yet on your local machine yet.

## Clone a Copy on Your Computer

The following steps will clone (create) a local copy of the forked repository on your computer.

1. Create a new folder in your computer that will contain `hackforla` projects.

In your command line interface (Terminal, Git Bash, Powershell), move to where you want your new folder to be placed and create a new folder in your computer that will contain `hackforla` projects. After that, navigate into the folder(directory) you just created.

For example:

```bash
cd /projects
mkdir hackforla
cd hackforla
```

2. From the hackforla directory created in previous section:

```bash
git clone https://github.com/<your_GitHub_user_name>/peopledepot.git
```

For example if your GitHub username was `octocat`:

```bash
git clone https://github.com/octocat/peopledepot.git
```

\*\*Note: You can also clone using ssh which is more secure but requires more setup. Because of the additional setup, cloning using https as shown above is recommended.

You should now have a new folder in your `hackforla` folder called `peopledepot`. Verify this by changing into the new directory:

```bash
cd peopledepot
```

## Verify and Setup Remote References

Verify that your local cloned repository is pointing to the correct `origin` URL (that is, the forked repo on your own Github account):

```bash
git remote -v
```

You should see `fetch` and `push` URLs with links to your forked repository under your account (i.e. `https://github.com/<your_GitHub_user_name>/peopledepot.git`). You are all set to make working changes to the website on your local machine.

However, we still need a way to keep our local repo up to date with the deployed website. To do so, you must add an upstream remote to incorporate changes made while you are working on your local repo. Run the following to add an upstream remote URL & update your local repo with recent changes to the `hackforla` version:

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

## Setup Docker

Install or make sure [docker][docker-install] and [docker-compose][docker-compose-install] are installed on your computer

```bash
    docker -v
    docker-compose -v
```

The recommended installation method for your operating system can be found [here](https://docs.docker.com/install/). <strong><em>Feel free to reach out in the [Hack for LA Slack channel](https://hackforla.slack.com/messages/people-depot/) if you have trouble installing docker on your system</em></strong>

More on using Docker and the concepts of containerization:

- [Get started with Docker](https://docs.docker.com/get-started/)

## Build and Run Using Docker Locally

**IMPORTANT:** Please make sure the `Docker Desktop` application is **running on your computer** before you run the bash commands below. Running `docker container ls` should list the peopledepot-web `image`, e.g.:
<img width="1698" alt="docker_ls_screenshot" src="https://user-images.githubusercontent.com/52610573/202492098-dd030a3b-12e5-4ccd-9d3e-65c13adaf953.png">

1. Create an .env.dev file from .env.dev-sample

   ```bash
   cp .env.dev-sample .env.dev
   ```

2. Build and run the project via the script (this includes running `docker-compose up`)

   ```bash
   ./scripts/buildrun.sh
   ```

3. Create a super user for logging into the web admin interface

   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

4. Browse to the web admin interface at `http://localhost:8000/admin/` and confirm the admin site is running. Use the credentials you created in Step 2 (above) to log in.

## Stopping Docker

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

# Working on an Issue

## Find an Issue

1. Find an issue in Prioritized Backlog [here](https://github.com/hackforla/peopledepot/projects/1)

If you joined the peopledepot repository as described in a previous section:

2. Assign the issue to yourself and move it to "In progress" column.
3. Follow the steps in the issue description to complete the issue.
4. Make sure to comment your ETA and Availability when you first assign yourself.

If you don't have privileges:

1. Add a comment that you are working on the issue.

## Create New Branch

Once you have selected an issue to work on, create a branch for that issue.

Verify you are on the `main` branch.

```bash
git branch
```

You will see a list of all of your branches. There will be a star (`*`) next to the branch that you are currently in. By default you should start on the `main` branch.

If you are not currently in the `main` branch, run the following command to return to it:

```bash
git checkout main
```

```bash
git pull origin main
```

This ensures you have the most recent code, which is important if you previously cloned and it has been more than a day.

Create a new branch where you will work on the issue. The branch name should include the issue number. For example, to create a new branch for issue 15 and change into it:

```bash
git checkout -b <new-branch-name>-15
```

## Make Changes

Make changes to fix the issue.

## Pull to Get Most Recent Code

You can probably skip this if you fix the issue on the same day that you pulled the code.

```bash
git pull
```

**Note:** If you are using Visual studios code you can use the Git graphical user interface to stage your changes. For instructions check out the [Git Gui Wiki](<https://github.com/hackforla/website/wiki/Using-Git-GUI-(Graphical-user-Interface)-in-Visual-Studios-Code>).

## Add Changed Files to Staging

**Make sure you are on your issue branch (instead of `main`)**

```bash
git branch
```

You must add your files to the staging area before you can commit (save them to git).

Run this command if you want to **add changes from a specific file to your commit record**:

```bash
git add “filename.ext”
```

Run this command if you want to **add all changes to all file(s) to your commit record**:

```bash
git add .
```

## Check git status

This command will list the files that have been staged with green text. These are the files that will be committed (saved) when you run the next command, `git commit`. Please be sure all your staged changes are relevant to the issue you are working on. If you accidentally included unrelated changes, please unstage them before making this commit, and then make a new commit for the unrelated changes. (The commands for unstaging commits are provided in the output of your `git status` command.)

```bash
git status
```

## Remove Files that you don't want Staged

This command will unstage a file that you don't want included in the commit. The specified file will not be committed (saved) when you run the next command, `git commit`. This only works if the wrong files were added, but they were not yet committed. (See [this tutorial](https://www.atlassian.com/git/tutorials/resetting-checking-out-and-reverting) for an in-depth discussion.) The file will be removed from the staging area, but not actually deleted:

```bash
git reset HEAD “filename.ext”
```

## Run pre-commit Checks

**Important: before committing each file, make sure to run the pre-commit hook:\***

```bash
./scripts/precommit-check.sh
```

## Commit Staged Changes

This command saves your work, and prepares it to push to your repository. Use the `-m` flag to quickly add a message to your commit. Your message should be a short description of the changes you made. It will be extremely helpful if other people can understand your message, so try to resist the temptation to be overly cryptic.

To commit your changes with a message, run:

```bash
git commit -m “insert message here”
```

Ensure that your local repository is up-to-date with the main site:

```bash
git pull upstream
```

You can also sync your fork directly on GitHub by clicking "Sync Fork" at the right of the screen and then clicking "Update Branch"

<details>
  <summary><strong>Click here</strong> to see how to sync the fork on GitHub</summary>
  <img src="https://docs.github.com/assets/cb-49937/images/help/repository/update-branch-button.png" />
</details>

## Push to Upstream (aka, your fork)

Push your local branch to your remote repository:

```bash
git push --set-upstream origin <your-branch-name>
```

Alternatively, you can run

```bash
git push
```

## Creating Pull Requests

### Push All Changes in your Issue Branch

Once you are satisfied with your changes, push them to the feature branch you made within your remote repository.

```bash
git push --set-upstream origin <name-of-branch>
```

### Complete pull request from Github

1. Click the green button to create a Pull Request (PR)
2. Add a short title in the subject line
3. In the body of the comment, add the following, replacing `<issue-number>` with the issue you worked on:

```bash
fixes #<issue-number>
```

4. Below this, add a brief description of the changes you made
5. Click the green "Create pull request" button
6. Add the PR to the project board

# Synch main Changes

Your fork of this repository on GitHub, and your local clone of that fork, will get out of sync with the (upstream) repository as others update the repository. (That's what has happened when you see something like "This branch is 1 commit behind peopledepot:main" on the github version of your hackforla repository.)

One way to keep your fork up to date with this repository is to follow these instruction: [Syncing your fork to the original repository via the browser](https://github.com/KirstieJane/STEMMRoleModels/wiki/Syncing-your-fork-to-the-original-repository-via-the-browser)

You can also update your fork via the local clone of your fork, using these instructions. Assuming you have a local clone with remotes `upstream` (this repo) and `origin` (your GitHub fork of this repo):

- First, you will need to create a local branch which tracks upstream/main. You will only need to do this once; you do not need to do this every time you want to incorporate upstream changes.

Run the following two commands:

```bash
git fetch upstream
git checkout -b upstream-main --track upstream/main
```

If you have already created the branch upstream-main, the following commands will incorporate upstream changes:

```bash
git checkout upstream-main # Move to the branch you want to merge with.
git pull  # This updates your tracking branch to match the main branch in this repository
git checkout main  # Move back to your main branch
git merge upstream-main  # Merge to bring your main current.
```

If you do all your work on topic branches (as suggested above) and keep main free of local modifications, this merge should apply cleanly.

Then push the merge changes to your GitHub fork:

```bash
git push
```

If you go to your online github repository this should remove the message "This branch is x commit behind peopledepot:main".

# Creating Issues

To create a new issue, please use the blank issue template (available when you click New Issue). If you want to create an issue for other projects to use, please create the issue in your own repository and send a slack message to one of your hack night hosts with the link.

# Pre-commit hooks

The pre-commit hook in git is currently a work in progress.

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

# Convenience scripts for sanity checks before committing code (assumes bash env)

1. buildrun.sh - clean, build, and run containers in background mode
1. lint.sh - lint and and auto-format code
1. test.sh - run tests and generate test coverage report
1. logs.sh - view/tail container logs
1. migrate.sh - run database migrations inside container
1. precommit-check.sh - sanity checks before committing code
1. createsuperuser.sh - creates a default superuser (assumes debian env.)

# Submitting Bugs for Third Party npm packages

You can go to these links and submit an issue:

[docker-install]: https://docs.docker.com/get-docker/
[docker-compose-install]: https://docs.docker.com/compose/install/
[flake8-docs]: https://github.com/pycqa/flake8
[black-docs]: https://github.com/psf/black
[isort-docs]: https://github.com/pycqa/isort/
