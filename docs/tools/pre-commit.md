# Pre-commit

The pre-commit hook in git will run before each commit and will abort the commit on failure. The advantage of this over GitHub Actions is that GitHub Actions work on code that's already committed, so it needs to allow code to be committed first.

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
