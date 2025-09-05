#!/bin/bash

set -e

echo "Waiting for database..."
while ! pg_isready -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER; do
	echo "Database is unavailable, wait . . ."
    sleep 2
done
echo "Database is up!"


echo "Waiting for Redis..."
while ! redis-cli -h $REDIS_HOST -p $REDIS_PORT ping; do
	echo "Redis is unavailable, wait . . ."
	sleep 2
done
echo "Redis is up!"


echo "Running migrations..."
python manage.py migrate --noinput


echo "Starting server..."
python manage.py runserver 0.0.0.0:8000