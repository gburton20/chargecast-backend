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

# Copy and set permissions for start script
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Collect static files (skip if fails)
RUN python manage.py collectstatic --noinput || echo "Static files collection skipped"

# Expose port
EXPOSE $PORT

# Run the startup script with bash explicitly
CMD ["/bin/bash", "/app/start.sh"]
