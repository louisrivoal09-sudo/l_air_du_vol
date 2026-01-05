import os
import sys
import django

# Get the absolute path of this file's directory (project root)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Add the django project directory to Python path
# The Django project is at: PROJECT_ROOT/louis/dblouis/
DJANGO_PROJECT_PATH = os.path.join(PROJECT_ROOT, 'louis', 'dblouis')

if DJANGO_PROJECT_PATH not in sys.path:
    sys.path.insert(0, DJANGO_PROJECT_PATH)

# Also add project root
if PROJECT_ROOT not in sys.path:
    sys.path.insert(1, PROJECT_ROOT)

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dblouis.settings')

# Debug logging
import logging
logger = logging.getLogger(__name__)
logger.info(f"WSGI: PROJECT_ROOT = {PROJECT_ROOT}")
logger.info(f"WSGI: DJANGO_PROJECT_PATH = {DJANGO_PROJECT_PATH}")
logger.info(f"WSGI: DJANGO_SETTINGS_MODULE = {os.environ.get('DJANGO_SETTINGS_MODULE')}")

# Setup Django
django.setup()

# Get the WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


