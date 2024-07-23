# Docker

## Working with Docker

### Stopping Docker

To stop the service-container, but not destroy it (often sufficient for day-to-day work):

```bash
docker-compose stop
```

To stop and destroy the service container:

```bash
docker-compose down
```

Add the `-v` flag to destroy the data volumes as well:

```bash
docker-compose down -v
```

### Recycling / Refreshing Database

To restore a database to its original state and remove any data manually added, delete the container and image.
From Docker:

=== "Terminal"
    ```bash
    docker-compose down -v
    ```

=== "Docker Desktop"
    1. Open Containers section
    1. Delete people-db-1 container
    1. Open Images Tab
    1. Remove djangorestapipostrgresql image

## Cache mount

This helps speed up subsequent docker builds by caching intermediate files and reusing them across builds. It's available with docker buildkit. The key here is to disable anything that could delete the cache, because we want to preserve it. The cache mount is not going to end up in the docker image being built, so there's no concern about disk space usage.

Put this flag between `RUN` and the command

```docker hl_lines="2"
RUN \
--mount=type=cache,target=/root/.cache
  pip install -r requirements.txt
```

For pip, the files are by default stored in `/root/.cache/pip`.  [Pip caching docs](https://pip.pypa.io/en/stable/topics/caching/)

For apk, the cache directory is `/var/cache/apk/`. [APK wiki on local cache](https://wiki.alpinelinux.org/wiki/Local_APK_cache)

For apt, the cache directory is `/var/cache/apt/`.

??? info "References"
    - [buildkit mount the cache](https://vsupalov.com/buildkit-cache-mount-dockerfile/)
    - [proper usage of mount cache](https://dev.doroshev.com/blog/docker-mount-type-cache/)
    - [mount cache reference](https://docs.docker.com/engine/reference/builder/#run---mounttypecache)
    - [buildkit dockerfile reference](https://github.com/moby/buildkit/blob/master/frontend/dockerfile/docs/reference.md)

## Alpine vs Debian based images

We're choosing to use an Alpine-based image for the smaller size and faster builds and downloads. However, a Debian-based image has the advantage of a large ecosystem of available packages, a limitation of Alpine that we may run up against in the future.

### Switching to Debian

Here is how we can switch to a Debian-based images if we need to:

1. Edit `Dockerfile` to look something like this

    ```Dockerfile title="app/Dockerfile"

    # pull official base image
    {--FROM python:3.10-alpine--}
    # (1)! define base image
    {++FROM python:3.10-bullseye++}

    # set work directory
    WORKDIR /usr/src/app

    # set environment variables
    ENV PYTHONDONTWRITEBYTECODE=1
    ENV PYTHONUNBUFFERED=1
    {++ENV PYTHONPYCACHEPREFIX=/root/.cache/pycache/++}
    {++ENV PIP_CACHE_DIR=/var/cache/buildkit/pip++}

    {++RUN mkdir -p $PIP_CACHE_DIR++}
    # (2)! prevent cache deletion
    {++RUN rm -f /etc/apt/apt.conf.d/docker-clean; \ ++}
    {++echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache++}

    # install system dependencies
    RUN \
    {--  --mount=type=cache,target=/var/cache/apk \ --}
    {--  --mount=type=cache,target=/etc/apk/cache \ --}
    {--  apk add \--}
    {--  'graphviz=~9.0'--}

    {--# install font for graphviz--}
    {--COPY Roboto-Regular.ttf /root/.fonts/--}
    {--RUN fc-cache -f--}
    # (3)! define cache mounts and install dependencies
    {++  --mount=type=cache,target=/var/cache/apt,sharing=locked \ ++}
    {++  --mount=type=cache,target=/var/lib/apt,sharing=locked \ ++}
    {++  apt-get update \ ++}
    {++  && apt-get install --no-install-recommends -yqq \ ++}
    {++  netcat=1.10-46 \ ++}
    {++  gcc=4:10.2.1-1 \ ++}
    {++  postgresql=13+225+deb11u1 \ ++}
    {++  graphviz=2.42.2-5++}

    # install dependencies
    COPY ./requirements.txt .
    # hadolint ignore=DL3042
    # (4)! install uv for faster dependency resolution
    RUN \
      --mount=type=cache,target=/root/.cache \
      pip install uv==0.1.15 \
      && uv pip install --system -r requirements.txt

    # copy entrypoint.sh
    COPY ./entrypoint.sh .
    RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh \
      && chmod +x /usr/src/app/entrypoint.sh

    # copy project
    COPY . .

    # run entrypoint.sh
    ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
    ```

    1. define base image
    1. prevent cache deletion
    1. install system dependencies
        1. define cache mounts for apt and lib
        1. install netcat for db wait script, which is used in `entrypoint.sh`
        1. install gcc for python local compiling, which shouldn't be needed
        1. install postgresql for `dbshell` management command
        1. install graphviz for generating ERD in `erd.sh`
    1. install uv for faster dependency resolution, which may or may not be wanted

1. Use the `dive` tool to check the image layers for extra files that shouldn't be there.
