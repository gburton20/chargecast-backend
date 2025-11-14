#!/bin/bash
set -e

echo "=== Starting ChargeCast Backend ==="
echo "Port: ${PORT}"

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Starting Gunicorn on 0.0.0.0:${PORT}..."
exec gunicorn chargecast_backend.wsgi:application \
    --bind "0.0.0.0:${PORT}" \
    --workers 2 \
    --threads 4 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level debug \
    --capture-output \
    --enable-stdio-inheritance
