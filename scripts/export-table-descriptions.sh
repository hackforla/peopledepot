#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

# Export all table descriptions to CSV
#
# Usage: ./export-table-descriptions.sh
#
# Output: table-descriptions.csv
# CSV format: table_name, column_name, data_type, is_nullable

CSV="table-descriptions.csv"
SQL="\\COPY (SELECT table_name, column_name, data_type, is_nullable
      FROM information_schema.columns
      WHERE table_schema = 'public'
      ORDER BY table_name, ordinal_position)
TO '/$CSV' WITH (FORMAT CSV, HEADER);"

set -x
docker compose exec db psql -d people_depot_dev -U people_depot -c "$SQL"
docker compose cp db:/$CSV .
