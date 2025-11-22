---
tags:
  - Django
  - migrations
  - git
---

# Resolve migration conflicts

When you're rebasing or merging branches, a conflict in `max_migration.txt` signals that numbered migration files are also conflicting. Normally, migrations with the same number would go undetected during a git merge/rebase because Django generates unique filenames for each one—but **`django-linear-migrations` surfaces this conflict by flagging it in `max_migration.txt`**.

You can resolve most migration conflicts using the [`rebase_migration`](https://github.com/adamchainz/django-linear-migrations#rebase_migration-command) command provided by the library.

## Step-by-step resolution

### Before you rebase

You're on your feature branch with all migrations applied and ready to rebase onto `upstream/main`.

1. **Start the rebase**

    ```bash
    git rebase upstream/main
    ```

    Git will pause and report a conflict in `core/migrations/max_migration.txt`.

1. **Note the conflicting migration numbers**

    For example, if the conflict involves `core/0025` and `core/0027`, the lowest number is `core/0025`. You'll need this later.

### Resolve the conflict

1. **Abort the rebase**

    ```bash
    git rebase --abort
    ```

1. **Roll back your local database** to the migration before the conflict

    Since the conflicting migrations need to be reapplied, roll back to the previous migration (e.g., `core/0024`):

    ```bash
    ./scripts/migrate.sh core 0024
    ```

1. **Restart the rebase**

    ```bash
    git rebase upstream/main
    # conflicts will appear again
    ```

1. **Auto-resolve migration conflicts**

    ```bash
    docker-compose exec web python manage.py rebase_migration core
    ```

1. **Resolve any code conflicts** manually as needed

1. **Reapply all migrations**

    ```bash
    ./scripts/migrate.sh core
    ```

1. **Run pre-commit checks**

    ```bash
    pre-commit run --all-files
    ```

1. **Stage your changes**

    ```bash
    git add <max_migration.txt> <changed migration files> <fixed code files>
    ```

1. **Complete the rebase**

    ```bash
    git rebase --continue
    ```

## When to use this

- **Updating a PR:** You've opened a PR and want to incorporate the latest changes from `upstream/main`
- **Merging a PR:** You're merging a feature branch and need to resolve migration conflicts with `upstream/main`

## Who should use this

- Developers and maintainers
