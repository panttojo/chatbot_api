#!/bin/sh
set -e

APP_MODULE="main:app"
HOST="0.0.0.0"
PORT="8000"
GUNICORN_WORKERS=2

echo "Starting Gunicorn with Uvicorn workers for $ENVIRONMENT environment..."
gunicorn "$APP_MODULE" \
    --workers "$GUNICORN_WORKERS" \
    --worker-class "uvicorn.workers.UvicornWorker" \
    --bind "$HOST":"$PORT" \
    --preload
