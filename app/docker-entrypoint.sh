#!/bin/bash -x

python manage.py  migrate --noinput || exit 1
python manage.py initialize_app
python manage.py runserver 0.0.0.0:8000
exec "$@"