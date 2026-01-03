import os
import sys
import django

# Chemin absolu du répertoire contenant ce fichier wsgi.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ajouter le répertoire 'louis' à sys.path (contient dblouis)
LOUIS_PATH = os.path.join(BASE_DIR, 'louis')
if LOUIS_PATH not in sys.path:
    sys.path.insert(0, LOUIS_PATH)

# Configurer Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dblouis.settings')

try:
    django.setup()
except Exception as e:
    print(f"Erreur lors du setup Django: {e}")
    print(f"LOUIS_PATH: {LOUIS_PATH}")
    print(f"sys.path: {sys.path}")
    raise

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
