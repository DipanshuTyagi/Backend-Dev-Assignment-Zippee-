#!/bin/sh
set -e

# Ensure data directory exists
mkdir -p /app/data

# Create the SQLite DB file if it doesn't exist
DB_FILE="/app/data/app.db"
if [ ! -f "$DB_FILE" ]; then
    echo "Creating empty SQLite DB at $DB_FILE"
    touch "$DB_FILE"
fi

# Start Gunicorn
exec ./gunicorn.sh
