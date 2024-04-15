# Docker

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
