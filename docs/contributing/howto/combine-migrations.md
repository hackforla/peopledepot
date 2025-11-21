---
tags:
  - Django
  - migrations
---

# Combine migrations

This howto assumes we have `django-linear-migrations` installed, and that we have a migration file `max_migration.txt` for each app that contains the latest migration for that app.

To combine migrations `0025-0027` in the `core` app, where the last migration is `0027`

1. Roll back migrations to before all the target migrations, e.g. `0024`

    ```bash
    ./script/migrate.sh core 0024
    ```

1. Delete migration files to be combined.

    ```bash
    rm app/core/migrations/00{25,26,27}_*
    ```

1. Recreate `max_migration.txt`

    ```bash
    docker-compose exec web python manage.py create_max_migration_files --recreate core
    # the file core/max_migration.txt should now contain "0024_..."
    ```

1. Generate combined migration file

    ```bash
    ./script/migrate.sh core
    ```

## When to use this

- PRs can have multiple migration files that should be made into a single create migration for merging.

## Who should use this

- Developers
