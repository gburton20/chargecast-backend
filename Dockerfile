# Use Python 3.12 slim image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files (skip if fails)
RUN python manage.py collectstatic --noinput || echo "Static files collection skipped"

# Expose port
EXPOSE $PORT

# Use shell form to ensure PORT variable is expanded
CMD python manage.py migrate && echo "Starting gunicorn on port $PORT" && gunicorn chargecast_backend.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120 --access-logfile - --error-logfile - --log-level debug --preload
