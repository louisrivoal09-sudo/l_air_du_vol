#!/bin/bash
cd louis/dblouis
gunicorn dblouis.wsgi:application --bind 0.0.0.0:$PORT
