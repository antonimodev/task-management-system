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

if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_EMAIL" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ] && [ "$DJANGO_SUPERUSER_NICKNAME" ]; then
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
user, created = User.objects.get_or_create(
	username='$DJANGO_SUPERUSER_USERNAME',
	email='$DJANGO_SUPERUSER_EMAIL',
	defaults={'nickname': '$DJANGO_SUPERUSER_NICKNAME'}
)
user.nickname = '$DJANGO_SUPERUSER_NICKNAME'
user.set_password('$DJANGO_SUPERUSER_PASSWORD')
user.is_superuser = True
user.is_staff = True
user.save()
END
fi

echo "Starting server..."
python manage.py runserver 0.0.0.0:8000
