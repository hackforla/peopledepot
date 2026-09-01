---
tags:
  - Docker
---

# Docker configuration

## Docker Compose

The project uses docker compose to run a local development environment.

The compose file is stored in the root of the project.

## Dockerfile

The Dockerfile is stored in the `app/` directory.

## Design

- We run Docker containers as a non-root user.
    - This is necessary for creating migration files not owned by root and usable by the normal user.
