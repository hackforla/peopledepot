---
tags:
    - AWS
    - deployment
    - Docker
---

# Test the AWS setup locally

Use `docker-compose-aws.yml` to build and run the production Docker image on your local machine before deploying to AWS. This exercises `Dockerfile-aws`, `entrypoint-aws.sh`, and `settings_aws.py` — catching configuration issues early.

The app runs on port **8001** so it can coexist with the standard dev environment on port 8000.

## Set up

1. Copy the example env file

    ```bash
    cp ./app/.env.docker-aws-example ./app/.env.docker-aws
    ```

1. Build and start the containers

    ```bash
    docker compose -f docker-compose-aws.yml up --build
    ```

    The build runs `collectstatic` and the entrypoint runs `migrate` automatically on startup.

1. Confirm the app is running by browsing to `http://localhost:8001/admin/`

## Stop and clean up

```bash
docker compose -f docker-compose-aws.yml down
```

To also remove the database volume:

```bash
docker compose -f docker-compose-aws.yml down -v
```

## Differences from the standard dev environment

| | `docker-compose.yml` | `docker-compose-aws.yml` |
|---|---|---|
| Image | Dev (`Dockerfile`) | Production (`Dockerfile-aws`) |
| Server | Django `runserver` | gunicorn |
| Settings | `settings.py` | `settings_aws.py` |
| Dependencies | `requirements.txt` | `requirements-aws.txt` |
| App port | 8000 | 8001 |
| DB port | 5432 | 5433 |
| Code reloading | Yes (volume mount) | No (baked into image) |
