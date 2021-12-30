#!/bin/sh
python manage.py migrate --no-input
python manage.py collectstatic --no-input
uwsgi --socket :8000 --module home_inventory.wsgi
