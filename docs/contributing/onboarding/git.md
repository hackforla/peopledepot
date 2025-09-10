# Working with Git

## Sync Main Changes

Your fork of this repository on GitHub, and your local clone of that fork, will get out of sync with the (upstream) repository as others update the repository. (That's what has happened when you see something like "This branch is 1 commit behind peopledepot:main" on your forked repository.)

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

If you go to your online GitHub repository this should remove the message "This branch is x commit behind peopledepot:main".
