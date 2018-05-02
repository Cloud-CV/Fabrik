#!/bin/sh
cd /code && \
python manage.py migrate --noinput && \
KERAS_BACKEND=theano python manage.py runserver 0.0.0.0:8000
