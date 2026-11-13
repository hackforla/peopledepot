# pull official base image
FROM python:3.10-alpine

# create non-root user and group
RUN addgroup -g 1000 app && \
  adduser -D -u 1000 -G app -h /home/app -s /bin/sh app

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPYCACHEPREFIX=/root/.cache/pycache/

# install system dependencies
RUN \
  --mount=type=cache,target=/var/cache/apk \
  --mount=type=cache,target=/etc/apk/cache \
  apk add \
  'graphviz=~12'

# install font for graphviz
COPY Roboto-Regular.ttf /root/.fonts/
RUN fc-cache -f

# install dependencies
COPY --chown=app:app ./requirements.txt .
# hadolint ignore=DL3042
RUN \
  --mount=type=cache,target=/root/.cache \
  pip install uv==0.1.15 \
  && uv pip install --system -r requirements.txt

# copy entrypoint.sh
COPY --chown=app:app ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh \
  && chmod +x /usr/src/app/entrypoint.sh

# copy project
COPY --chown=app:app . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
