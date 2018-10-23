#!/bin/sh
cd /code && \
python manage.py makemigrations caffe_app && \
python manage.py migrate --noinput && \
python manage.py collectstatic --noinput
uwsgi --ini /code/docker/prod/django/uwsgi.ini & daphne -b 0.0.0.0 -p 8001 -v 1 --websocket_timeout 86400 --websocket_connect_timeout 10 --access-log log-daphne.log ide.asgi:channel_layer & python manage.py runworker
