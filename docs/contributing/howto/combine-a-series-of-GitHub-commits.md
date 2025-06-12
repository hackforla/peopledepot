# Combine a series of GitHub commits into one commit 

This is a quick way of combining a series of GitHub commits into one:

1. Assume we're at the head of the PR branch with 4 commits and want to combine the 4 commits into one.
1. Soft reset to the earliest commit, with all the changes of the later commits staged.
    ```bash
    git reset --soft HEAD~3
    ```
1. Amend the staged changed into the earliest commit.
    ```bash
    git commit --amend --no-edit
    ```
    **note**: omit the `--no-edit` flag if you want to edit the commit message.

Although there are other ways of combining GitHub commits (like `lazygit` and the standard interactive rebase),  these are more interactive than the process described above and therefore more difficult to describe in text form. 

####  Where would this information have been useful?
- https://github.com/hackforla/peopledepot/pull/398/commits contained 4 commits, which were then merged into one before rebasing it to `main`, in order to make it easier to work with.
- This info could be useful when dealing with PRs that need to be rebased to `upstream/main`, especially when there are also migration conflicts in which more than one commit in the PR contains migration files. If the PR commits are all merged into one, the migration conflicts can be simplified along with the repetitive need to resolve merges.

#### Which roles will benefit most from this information?
- Backend
- Dev