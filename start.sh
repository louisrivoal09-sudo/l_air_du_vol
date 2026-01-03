#!/bin/bash
set -e
cd /opt/render/project/src/louis/dblouis
python manage.py migrate --no-input
gunicorn dblouis.wsgi:application --bind 0.0.0.0:$PORT
