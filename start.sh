#!/bin/bash
set -e

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Starting Gunicorn server on port ${PORT:-8000}..."
exec gunicorn chargecast_backend.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 2 \
    --threads 4 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    --capture-output \
    --enable-stdio-inheritance
