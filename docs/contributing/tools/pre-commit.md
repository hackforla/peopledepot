# Pre-commit

The hooks will run when doing normal `git commit` and `git push` commands. It's recommended to do this in the command line to see the output. If performing these actions from a gui application, the interface may seem to hang for some time.

The pre-commit checks should be fast while the pre-push hooks will take longer since they'll do a full rebuild

## Installation

It's recommended to install "global" tools via pipx, which installs packages in an isolated environment rather than the global python environment.

1. [Install pipx](https://pipx.pypa.io/latest/installation/)

1. Install pre-commit

    ```bash
    pipx install pre-commit
    ```

1. Add the hook to git

    ```bash
    pre-commit install
    ```

    Pre-commit is now set up to check your files whenever you commit or push code.

1. Test by adding an empty commit

    ```bash
    git commit --allow-empty -m "Test"
    ```

    You should see a list of tests that are all skipped, because there's no changes in the commit to test.

## Extra information

- To skip the checks temporarily, you can do one of these

    ```bash
    # skip all the hooks
    git commit --no-verify

    # skip specific hooks
    SKIP=black,flake8 git commit
    ```

- Manually run the hooks (this runs it against all files rather than only changed files)

    ```bash
    pre-commit run --all-files
    ```

- More commands to run the hooks

    ```bash
    # run the hooks for the push staga
    pre-commit run --all-files --hook-stage push

    # run the hooks for the commit stage
    pre-commit run --all-files --hook-stage commit

    # run the hooks for
    pre-commit run test --all-files --hook-stage push
    ```

- Update pre-commit and plugins to the latest version

    ```bash
    pre-commit autoupdate
    ```
