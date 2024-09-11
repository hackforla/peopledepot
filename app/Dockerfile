# pull official base image
FROM python:3.10-bullseye

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPYCACHEPREFIX=/root/.cache/pycache/
ENV PIP_CACHE_DIR=/var/cache/buildkit/pip

RUN mkdir -p $PIP_CACHE_DIR
RUN rm -f /etc/apt/apt.conf.d/docker-clean; echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache

# install system dependencies

# hadolint ignore=DL3008
RUN \
  --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
  apt-get update \
  && apt-get install --no-install-recommends -yqq \
  netcat=1.10-46 \
  gcc=4:10.2.1-1 \
  graphviz

# install dependencies
COPY ./requirements.txt .
# hadolint ignore=DL3042
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
