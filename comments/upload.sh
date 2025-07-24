#!/bin/bash

DB_NAME="regulations_comments"
TABLE="comments"
USER="postgres"
DATA_DIR="/comment_data"

echo "Importing CSV files from $DATA_DIR into $TABLE..."

for file in "$DATA_DIR"/*.csv; do
  echo "Importing $file..."
  psql -U "$USER" -d "$DB_NAME" -c "\COPY $TABLE FROM '$file' CSV HEADER;"
done

echo "Done importing."

