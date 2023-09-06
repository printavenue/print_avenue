#!/bin/bash
echo "Creating Migrations..."
python manage.py makemigrations
echo ====================================

echo "Starting Migrations..."
python manage.py migrate
echo ====================================

echo "Creating admin user admin@gmail.com:admin"
python manage.py createadmin admin@gmail.com admin
echo ====================================

echo "Starting Server..."
python manage.py runserver 0.0.0.0:8000 & celery -A print_avenue worker --loglevel=info