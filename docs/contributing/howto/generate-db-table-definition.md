---
tags:
  - database
  - postgres
---

# Generate database table description

!!! note

    This guide works only for the postgres database running locally in a Docker container.

#### Short way (single command)

!!! note "(Optional) Get all table names"

    This is helpful for getting a list of table names to use in the next command.

    ```bash
    ./scripts/db.sh -c "\dt"
    ```

1. Get table description

    This command prints the table description to the terminal.

    ```bash
    ./scripts/db.sh -c "\d <table_name>"
    ```

    Example table name: `core_user`

    ```bash
    ./scripts/db.sh -c "\d core_user"
    ```

#### Long way (interactive)

1. Enter the database shell in the docker container (\\q to exit)

    ```
    ./scripts/db.sh
    ```

1. Get list of tables

    ```
    \dt
    ```

1. Get table description

    ```
    \d <table_name>
    ```
