#!/bin/bash
echo SQL USER $SQL_USER
export file=$1
echo "file = $file / $1 / $2"
if [ "$file" == "" ]
then
  echo "File not specified.  Using .env.local"
  file=".env.local"
fi

echo "Loading environment variables from $file"

if [ ! -f $file ]
then
  echo "File $file not found"
  echo "If executing locally, copy .env.example.dev to $file and edit as needed"
  return 1
fi
while IFS= read -r line; do
  if [[ -n "$line" ]]; then
    echo "export $line"
    export "$line"
  fi
done < <(grep -v '^#' "$file")
echo Super user $DJANGO_SUPERUSER_USERNAME
echo Settings module $DJANGO_SETTINGS_MODULE
echo SQL USER $SQL_USER
