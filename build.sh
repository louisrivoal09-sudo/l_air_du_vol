#!/bin/bash
set -o errexit

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Navigate and collect static files
cd louis/dblouis
python manage.py collectstatic --no-input
