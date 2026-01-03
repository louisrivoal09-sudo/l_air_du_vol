import os
import sys
import django

# Ajouter le chemin vers louis/dblouis
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, 'louis', 'dblouis'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dblouis.settings')

django.setup()

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
