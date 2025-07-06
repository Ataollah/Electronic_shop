#!/bin/bash
# Exit on any error
set -e

# Run database migrations
#python manage.py makemigrations --noinput
python manage.py migrate

# Create superuser if it doesn't exist
echo "from django.contrib.auth import get_user_model; \
User = get_user_model(); \
User.objects.filter(username='admin').exists() or \
User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')" | python manage.py shell

# Start the application
exec "$@"