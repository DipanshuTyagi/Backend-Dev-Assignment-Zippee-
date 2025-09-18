#!/bin/sh
set -e

WORKERS=${WORKERS:-4}
THREADS=${THREADS:-2}
HOST=${HOST:-0.0.0.0}
PORT=${PORT:-5000}

echo "Starting Gunicorn on $HOST:$PORT with $WORKERS workers and $THREADS threads..."
exec uv run gunicorn \
    --workers $WORKERS \
    --threads $THREADS \
    --bind $HOST:$PORT \
    app.main:app
