---
tags:
  - Django
  - migrations
---

# Resolve migration conflict

Let's say you're rebasing and the `max_migration.txt` file shows a conflict. That's a sign that the numbered migration files are conflicting as well. They're named differently so their conflicts don't show up in git.

In many cases, you can resolve migration conflicts by using the `rebase_migration` command provided by [`django-linear-migrations`](https://github.com/adamchainz/django-linear-migrations).

Assume you're at your feature branch and all migrations are applied.

1. Rebase your branch to `upstream/main`

    ```bash
    git rebase upstream/main
    ```

1. See if there's a conflict in `core/migrations/max_migration.txt` and note the lowest migration number to be used later.

1. If it does show a conflict(e.g., between `core/0025` and `core/0027`), undo the rebase.

    You'd have migrations applied that are part of the conflict. You need to roll the database back to a point before that, so you can change those migrations if necessary.

    ```bash
    git rebase --abort
    ```

1. Roll back the local database to a previous migration (any number before the ones in conflict)

    ```bash
    ./scripts/migrate.sh core 0024
    ```

1. Re-run the rebase

    ```bash
    git rebase upstream/main
    # see conflicts returned
    ```

1. Resolve the migration conflict

    ```bash
    docker-compose exec web python manage.py rebase_migration core
    ```

1. Resolve any code conflicts

1. Run all the migrations

    ```bash
    ./scripts/migrate.sh core
    ```

1. Run pre-commit checks

    ```bash
    pre-commit run —all-files
    ```

1. Stage all the fixes

    ```bash
    git add <max_migration.txt> <changed migration files> <fixed code files>
    ```

1. Continue rebase

    ```bash
    git rebase --continue
    ```

## When to use this

- This is helpful for anyone who has created a PR and then wants to update it with the latest changes from `upstream/main`
- It's useful for someone merging a PR and needs to resolve migration conflicts between the feature branch and `upstream/main`

## Who should use this

- Developers, Maintainers
