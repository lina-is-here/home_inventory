#!/bin/sh
python manage.py migrate --no-input
python manage.py collectstatic --no-input
uwsgi --socket :8000 --uid=1001 --gid=1001 --master --module home_inventory.wsgi --vacuum
