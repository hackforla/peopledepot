#!/bin/bash
set -euo pipefail
IFS=$'\n\t'
set -x

# create entity-relation diagram
docker compose exec web python manage.py graph_models -a > app/erd.dot
docker compose exec web dot -Tpng erd.dot -o erd.png
# docker compose exec web python manage.py graph_models --pydot -a -g -o erd.png
