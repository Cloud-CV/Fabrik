#!/bin/sh
cd /code && \
webpack && \

KERAS_BACKEND=theano supervisord -n
