import os
import sys
import django

# Ajouter le chemin vers le projet Django avant tout import Django
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOUIS_PATH = os.path.join(BASE_DIR, 'louis')

# Assurez-vous que le chemin du projet est d'abord dans sys.path
if LOUIS_PATH not in sys.path:
    sys.path.insert(0, LOUIS_PATH)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dblouis.settings')
django.setup()

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
