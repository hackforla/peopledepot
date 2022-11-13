# How to Contribute to PeopleDepot

Thank you for volunteering your time! The following is a set of guidelines for contributing to the peopledepot repository, which is hosted on GitHub. 

**Please make sure you have completed the onboarding process which includes joining the Hack for LA Slack, GitHub, and Google Drive. If you have not been onboarded, see the [Getting Started Page](https://www.hackforla.org/getting-started).** _Workshop attendees are granted a temporary exception from this requirement._ 

You will need the following to get started:

- a [GitHub account](https://docs.github.com/en/get-started/signing-up-for-github/signing-up-for-a-new-github-account#signing-up-for-a-new-account)
- A text editor. [PyCharm](https://www.jetbrains.com/pycharm/download/#section=mac) is a common Python IDE. [VS Code](https://code.visualstudio.com/download) is another common editor. Feel free to use a text editor of your choice.

## **Part 1: Setting up the development environment**

### **1.1 Dev setup (1): Join the repository team**

In the `hfla-site` Slack channel, send an introductory message with your GitHub handle/username asking to be added to the Hack for LA peopledepot GitHub repository.

**NOTE:** Once you have accepted the GitHub invite (comes via email or in your GitHub notifications), **please do the following**:

1. Make your own Hack for LA GitHub organization membership public by following this [guide](https://help.github.com/en/articles/publicizing-or-hiding-organization-membership#changing-the-visibility-of-your-organization-membership).
2. Set up two-factor authentication on your account by following this [guide](https://docs.github.com/en/github/authenticating-to-github/configuring-two-factor-authentication).

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

## **Part 2: Working on issues**

### **2.1 Finding an issue to work on**

1. Find an issue in Prioritized Backlog [here](https://github.com/hackforla/peopledepot/projects/1)
2. Assign the issue to yourself and move it to "In progress" column.
3. Follow the steps in the issue description to complete the issue.
4. Make sure to comment your ETA and Availability when you first assign yourself.

### **2.2 Working on an issue**

#### **2.2.a Working on an issue(1): Verifying current branch**
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

Create a new branch where you will work on the issue. The branch name should include the issue number. For example, to create a new branch for issue 15 and change into it:

```bash
git checkout -b <new-branch-name>-15
```

#### **2.2.b Working on an issue(2): Prepare your changes to push to your repository**

Once you are done with the work on your issue you will push it to your repository.  Before you can push your work to your repository, you will stage and commit your changes.  These two commands are similar to the save command used in other programs. 

**Note:** If you are using Visual studios code you can use the Git graphical user interface to stage your changes. For instructions check out the [Git Gui Wiki](https://github.com/hackforla/website/wiki/Using-Git-GUI-(Graphical-user-Interface)-in-Visual-Studios-Code).

**Note:** Remember to run the `precommit-checks.sh` script before each commit until it can be integrated.

#### **i. Prepare repo changes (1): Use the `git add` command to stage your changes.** 

**Make sure you are on your issue branch (instead of `main`)**

This command prepares your changes before you commit them. You can stage files one at a time using the filename. 

Run this command if you want to **add changes from a specific file to your commit record**: 
```bash
git add “filename.ext”
```

Run this command if you want to **add all changes to all file(s) to your commit record**: 
```bash
git add .
```

#### **ii. Prepare repo changes (2): Use the `git status` command to see what files are staged.**

This command will list the files that have been staged.  These are the files that will be committed (saved) when you run the next command, `git commit`. Please be sure all your staged changes are relevant to the issue you are working on. If you accidentally included unrelated changes, please unstage them before making this commit, and then make a new commit for the unrelated changes. (The commands for unstaging commits are provided in the output of your `git status` command.)
      
```bash
git status
```

##### **iii. Prepare repo changes (3): Use the `git reset HEAD` command to remove a staged file.**

This command will remove a file that has been staged.  This file will not be committed (saved) when you run the next command, `git commit`. This only works if the wrong files were added, but they were not yet committed. The file will be removed from the staging area, but not actually deleted:

```bash
git reset HEAD “filename.ext” 
```
##### **iv. Prepare repos changes (4): Use the `git commit` command**

This command saves your work, and prepares it to push to your repository.  Use the `-m` flag to quickly add a message to your commit. Your message should be a short description of the changes you made.  It will be extremely helpful if other people can understand your message, so try to resist the temptation to be overly cryptic.

For linting and code formatting, run:
```bash
./scripts/lint.sh
```

**Important: before committing each file, make sure to run the pre-commit hook:***

```bash
./scripts/precommit-check.sh
```

To commit your changes with a message, run:

```bash
git commit -m “insert message here”
```

**IMPORTANT:** Before you push your local commits to your repository, sync your fork to the main Hack For LA peopledepot repository. Ensure that your local repository is up-to-date with the main site:

```bash
git pull upstream
```
You can also sync your fork directly on GitHub by clicking "Sync Fork" at the right of the screen and then clicking "Update Branch"

<details>
  <summary><strong>Click here</strong> to see how to sync the fork on GitHub</summary>
  <img src="https://docs.github.com/assets/cb-49937/images/help/repository/update-branch-button.png" />
</details>

##### **i. If there are no changes in the upstream repository**

If you do not see any output, there have not been any changes in the main Hack for LA peopledepot repository since the last time you
checked. So it is safe to push your local commits to your fork.

Push your local branch to your remote repository:

```bash
git push --set-upstream origin <your-branch-name>
```

Alternatively, you can run

```bash
git push
```

This will provide the code to create a new branch in your GitHub repository. Copy the command and paste it into your terminal and press enter to run it.

##### **ii. If there are conflicting changes in the upstream repository**

When you check the upstream repository, you may see output like this:

```bash
remote: Enumerating objects: 184, done.
remote: Counting objects: 100% (184/184), done.
remote: Compressing objects: 100% (62/62), done.
remote: Total 184 (delta 123), reused 162 (delta 122), pack-reused 0
Receiving objects: 100% (184/184), 26.75 KiB | 6.69 MiB/s, done.
Resolving deltas: 100% (123/123), completed with 43 local objects.
From https://github.com/hackforla/peopledepot
 * [new branch]      develop    -> upstream/develop
   56e6dc7..923215d  main       -> upstream/main

```


**Note:** You can safely ignore changes in other issue branches, such as `develop` above. But if you see changes in `main`, as in `56e6dc7..923215d main   -> upstream/main`, you should incorporate those changes into your repository before merging or rebasing your issue branch. Use the [instructions below](#22c-working-on-an-issue-3-incorporating-changes-from-upstream) to bring your fork up to date with the main repository.

#### **2.2.c Working on an issue (3): Pulling from upstream before you push**

Your fork of this repository on GitHub, and your local clone of that fork, will get out of sync with this (upstream) repository from time to time. (That's what has happened when you see something like "This branch is 1 commit behind peopledepot:main" on the github version of your hackforla repository.)

One way to keep your fork up to date with this repository is to follow these instruction: [Syncing your fork to the original repository via the browser](https://github.com/KirstieJane/STEMMRoleModels/wiki/Syncing-your-fork-to-the-original-repository-via-the-browser)

You can also update your fork via the local clone of your fork, using these instructions. Assuming you have a local clone with remotes `upstream` (this repo) and `origin` (your GitHub fork of this repo):

* First, you will need to create a local branch which tracks upstream/main.  You will only need to do this once; you do not need to do this every time you want to incorporate upstream changes. 

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

### **2.3 Creating a new issue**

To create a new issue, please use the blank issue template (available when you click New Issue).  If you want to create an issue for other projects to use, please create the issue in your own repository and send a slack message to one of your hack night hosts with the link.

## **Part 3: Creating Pull Requests**

### **3.1 How to make a pull request**

#### **3.1.a Push all changes to your issue branch**

Once you are satisfied with your changes, push them to the feature branch you made within your remote repository. 

```bash
git push --set-upstream origin <name-of-branch>
```

#### **3.1.b Complete pull request on Hack for LA `peopledepot` repo**

1. Click the green button to create a Pull Request (PR)
2.  Add a short title in the subject line
3. In the body of the comment, add the following, replacing <issue-number> with the issue you worked on:

```bash
fixes #<issue-number>
```
4. Below this, add a brief description of the changes you made
5. Click the green "Create pull request" button
6. Add the PR to the project board 

## Testing

1. Run all tests from the project root

    ```bash
    ./scripts/test.sh
    ```

## Linting and autoformatting

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

#### Submit a bug

#### Submit a feature request

[docker-install]: https://docs.docker.com/get-docker/
[docker-compose-install]: https://docs.docker.com/compose/install/
[flake8-docs]: https://github.com/pycqa/flake8
[black-docs]: https://github.com/psf/black
[isort-docs]: https://github.com/pycqa/isort/
