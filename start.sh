#!/bin/bash
set -e
python louis/dblouis/manage.py migrate --no-input
gunicorn wsgi:application --bind 0.0.0.0:$PORT
