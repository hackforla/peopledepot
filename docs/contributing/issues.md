# Fixing Issues

## Find an issue

Find an issue in Prioritized Backlog [here](https://github.com/hackforla/peopledepot/projects/1#column-16900748)

If you joined the peopledepot repository as described in a previous section:

1. Assign the issue to yourself and move it to "In progress" column.
1. Follow the steps in the issue description to complete the issue.
1. Make sure to comment your ETA and Availability when you first assign yourself.

If you don't have privileges, add a comment that you are working on the issue.

## Create a new branch

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

## Make changes

Make changes to fix the issue.

## Pull to get the most recent code

You can probably skip this if you fix the issue on the same day that you pulled the code.

```bash
git pull
```

!!! note "If you are using Visual studios code you can use the Git graphical user interface to stage your changes. For instructions check out the [Git GUI page in the website Wiki](<https://github.com/hackforla/website/wiki/How-to-Use-Git-GUI-(Graphical-user-Interface)-in-Visual-Studios-Code>)"

## Add changed files to staging

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

## Check Git status

This command will list the files that have been staged with green text. These are the files that will be committed (saved) when you run the next command, `git commit`. Please be sure all your staged changes are relevant to the issue you are working on. If you accidentally included unrelated changes, please unstage them before making this commit, and then make a new commit for the unrelated changes. (The commands for unstaging commits are provided in the output of your `git status` command.)

```bash
git status
```

## Remove files that you don't want staged

This command will unstage a file that you don't want included in the commit. The specified file will not be committed (saved) when you run the next command, `git commit`. This only works if the wrong files were added, but they were not yet committed. (See [this tutorial](https://www.atlassian.com/git/tutorials/resetting-checking-out-and-reverting) for an in-depth discussion.) The file will be removed from the staging area, but not actually deleted:

```bash
git reset HEAD “filename.ext”
```

## Install pre-commit

This will check your changes for common problems.

See the [Pre-commit page](tools/pre-commit.md) for installation instructions.

For consistency, an automated bot will perform the same checks on the repository side when you open a pull request.

## Commit staged changes

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

## Push to upstream origin (aka, your fork)

Push your local branch to your remote repository:

```bash
git push --set-upstream origin <your-branch-name>
```

Alternatively, you can run

```bash
git push
```

## Create a pull request

### Push all changes in your issue branch

Once you are satisfied with your changes, push them to the feature branch you made within your remote repository.

```bash
git push --set-upstream origin <name-of-branch>
```

### Complete pull request from GitHub

1. Click the green button to create a Pull Request (PR)
1. Add a short title in the subject line
1. In the body of the comment, add the following, replacing `<issue-number>` with the issue you worked on:

```bash
fixes #<issue-number>
```

1. Below this, add a brief description of the changes you made
1. Click the green "Create pull request" button
1. Add the PR to the project board

# Creating Issues

To create a new issue, please use the blank issue template (available when you click New Issue). If you want to create an issue for other projects to use, please create the issue in your own repository and send a slack message to one of your hack night hosts with the link.
