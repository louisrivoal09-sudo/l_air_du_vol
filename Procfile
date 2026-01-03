release: cd louis/dblouis && python manage.py migrate
web: cd louis/dblouis && gunicorn dblouis.wsgi:application --bind 0.0.0.0:$PORT
