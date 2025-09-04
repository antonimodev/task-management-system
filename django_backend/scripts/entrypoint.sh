#!/bin/bash

set -e

echo "Waiting for database..."
while ! pg_isready -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER; do
	echo "Database is unavailable, wait . . ."
    sleep 2
done
echo "Database is up!"


echo "Waiting for Redis..."
while ! redis-cli -h $REDIS_HOST -p $REDIS_PORT ping > /dev/null 2>&1; do # Testear sin dev/null o sin 2>&1
	echo "Redis is unavailable, wait . . ."
	sleep 2
done
echo "Redis is up!"


echo "Running migrations..."
python manage.py migrate --noinput

#ESTO SE USARA MAS ADELANTE CUANDO HAYA ARCHIVOS ESTATICOS EN FRONTEND
#echo "Collecting static files..."
#python manage.py collectstatic --noinput # not sure about introduce --clear

echo "Starting server..."
# exec gunicorn --bind 0.0.0.0:8000 --workers 4 myproject.wsgi:application ¿QUITAR? En principio es utilizado en produccion
python manage.py runserver 0.0.0.0:8000