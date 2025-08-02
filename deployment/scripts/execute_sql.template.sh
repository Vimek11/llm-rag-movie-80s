#!/bin/bash
set -e

echo "Running SQL scripts on PostgreSQL..."

export PGPASSWORD=#{PG_PASSWORD}#

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SQL_DIR="$SCRIPT_DIR/sql"

FILES=$(echo #{SQL_FILES}# | tr "," "\n")

for file in $FILES; do
  echo "Executing $file..."
  psql -h "#{PG_HOST}#" -p "#{PG_PORT}#" -U "#{PG_USER}#" -d "#{PG_DATABASE}#" -f "$SQL_DIR/$file"
done

echo "All SQL scripts executed successfully."
