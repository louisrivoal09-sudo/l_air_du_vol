#!/bin/bash
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
cd louis/dblouis
python manage.py collectstatic --no-input
python manage.py migrate --no-input
