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

1. Edit `.env.docker-aws` and set a real `SECRET_KEY` — don't leave the placeholder value

1. Build and start the containers

    ```bash
    docker compose -f docker-compose-aws.yml up --build
    ```

    The build runs `collectstatic` and the entrypoint runs `migrate` automatically on startup.

1. Verify it's running correctly

    - Browse to `http://localhost:8001/admin/` — you should see the Django admin login page (not a 500 or connection error), styled with CSS (not unstyled HTML — confirms `collectstatic`/whitenoise are working)
    - `curl http://localhost:8001/api/v1/` should return a JSON response, not a 404 or 500
    - `http://localhost:8001/api/schema/swagger-ui/` should 404(Not Found) — `urls_aws.py` intentionally excludes schema routes from production

1. Create a superuser to log into the admin interface (in a separate terminal)

    ```bash
    docker compose -f docker-compose-aws.yml exec web python manage.py createsuperuser
    ```

    Logging in successfully at `http://localhost:8001/admin/` confirms migrations ran and the database is up.

## Stop and clean up

```bash
docker compose -f docker-compose-aws.yml down
```

To also remove the database volume:

```bash
docker compose -f docker-compose-aws.yml down -v
```

!!! note "Network warning"

    You may see `! Network peopledepot_default Resource is still in use` — this is harmless. The containers and volume are already removed. The network is shared with the dev `docker-compose.yml` stack (the mkdocs container keeps it alive) and will clean up when that stack is stopped.

## Gotchas

!!! warning

    - `requirements-aws.txt` must be compiled with `--python-version 3.10` — compiling locally can resolve packages incompatible with the Docker image's Python version
    - Do not mount `./app/` as a volume — it would bypass `collectstatic`, the multi-stage build, and `settings_aws.py`
    - `.env.docker-aws` sets `SECURE_SSL_REDIRECT=False`; real production sets it `True`. Don't flip it to `True` locally — without SSL it causes an infinite redirect loop
    - `drf_spectacular` stays in `requirements-aws.txt` even though it's excluded from `INSTALLED_APPS` — it's still a runtime import in `views.py` decorators, and the container crashes without it
    - `DEBUG=False` is intentional — don't change it; the point of this setup is to test production behavior

## Differences from the standard dev environment

|                | `docker-compose.yml` | `docker-compose-aws.yml`      |
| -------------- | -------------------- | ----------------------------- |
| Image          | Dev (`Dockerfile`)   | Production (`Dockerfile-aws`) |
| Server         | Django `runserver`   | gunicorn                      |
| Settings       | `settings.py`        | `settings_aws.py`             |
| Dependencies   | `requirements.txt`   | `requirements-aws.txt`        |
| App port       | 8000                 | 8001                          |
| DB port        | 5432                 | 5433                          |
| DB volume      | `postgres_data`      | `postgres_data_aws`           |
| Code reloading | Yes (volume mount)   | No (baked into image)         |
| Schema UI      | Available            | Excluded (`urls_aws.py`)      |
