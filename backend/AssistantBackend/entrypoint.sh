#!/bin/sh

# Stop on error
set -e

# Apply database migrations
echo "Making migrations..."
python manage.py makemigrations

echo "Applying migrations..."
python manage.py migrate --noinput

# Start the Django server
echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000
