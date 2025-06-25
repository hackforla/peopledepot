#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

# Export all table descriptions to CSV
#
# Usage: ./export-table-descriptions.sh [optional filename]
#
# Output: table-descriptions.csv unless a filename is specified
# CSV format: table_name, column_name, data_type, is_nullable

csv_file="table-descriptions.csv"
if [ $# -gt 0 ]; then
      csv_file=$1
fi
SQL="\\COPY (SELECT table_name, column_name, data_type, is_nullable
      FROM information_schema.columns
      WHERE table_schema = 'public'
      ORDER BY table_name, ordinal_position)
TO '/$csv_file' WITH (FORMAT CSV, HEADER);"

set -x
docker compose exec db psql -d people_depot_dev -U people_depot -c "$SQL"
docker compose cp db:/"$csv_file" .
