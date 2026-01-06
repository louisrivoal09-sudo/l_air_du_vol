"""
WSGI application entry point for Vercel serverless functions
"""
import os
import sys
from pathlib import Path

# Add the project directory to the Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dblouis.settings')

# Setup Django
import django
django.setup()

from django.core.wsgi import get_wsgi_application

# Get the WSGI application
app = get_wsgi_application()

# Export the handler for Vercel
def handler(request):
    """Handler for Vercel serverless functions"""
    return app(request)
