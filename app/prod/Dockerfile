FROM python:3.11-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apk update && \
    apk add --no-cache netcat-openbsd gcc postgresql graphviz musl-dev libffi-dev

# install dependencies
RUN pip install --no-cache-dir pip~=21.3.1
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# # copy entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]

