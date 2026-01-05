release: cd louis/dblouis && python manage.py migrate --no-input
web: gunicorn wsgi:application --bind 0.0.0.0:$PORT --workers 2
