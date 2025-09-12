# Pre-commit

The hooks will run when doing normal `git commit` and `git push` commands. It's recommended to do this in the command line to see the output. If performing these actions from a gui application, the interface may seem to hang for some time.

The pre-commit checks should be fast while the pre-push hooks will take longer since they'll do a full rebuild

## Installation

It's recommended to install "global" tools via pipx, which installs packages in an isolated environment rather than the global python environment.

1. [Install uv](uv.md)

1. Install pre-commit

    ```bash
    uv tool install pre-commit --with pre-commit-uv
    ```

    [Source guide](https://adamj.eu/tech/2025/05/07/pre-commit-install-uv/)

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

## Helpful automations

??? note "Autofix file line endings to LF"

    We use LF line endings since the code is designed to run on Linux. We're forcing this to happen so speed up our PR review process. Individual developers should still set up their editors to use LF line endings.

    We do this via the following lines in `git-commit-hooks`:

    ```bash
    - id: mixed-line-ending
    args: [--fix=lf]
    exclude: ^app/core/initial_data/
    ```

    Note that we're excluding the initial data from this check for now since we're not decided on the correct line ending there.

## Disabled rules

Sometimes, we need to disable a few specific rules that are causing problems. We list them here along with information about them.

??? info "FLAKE8 EXE002"

    This rule is part of flake8's flake8-executable plugin. It checks that all executable scripts have shebangs. This is to ensure that we don't create executable scripts (setting the executable bit) that we don't want to be executable (omitting the shebang).

    We disable this rule for the following reasons:

    1. The rule is broken for NTFS files.
    1. The rule is a duplicate of the `check-executables-have-shebangs` rule in the `pre-commit-hooks` repo.
        - that rule [does work with NTFS](https://github.com/pre-commit/pre-commit-hooks/pull/480) by checking the repository metadata for the file, which has the correct executable bit data.

    The rule works correctly in these environments:

    - Windows (WSL)
    - Linux
    - macOS

    The rule fails under this specific combination of conditions:

    1. The developer is on a Windows system.
    1. The developer is using git bash.
    1. The developer cloned the repository to an NTFS directory (C:\\ or D:) rather than to a linux filesystem (under WSL).

    This rule is broken in the following way:

    1. It asks the operating system to check if the file is executable and checks the file for a shebang. But NTFS does not have the notion of the executable bit, and will always return `True` for all files. So files like `app/core/admin.py` that's not meant to be executable will look like they are executable, and cause the rule to fail, because it doesn't contain a shebang.
