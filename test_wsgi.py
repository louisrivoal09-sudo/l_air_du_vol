#!/usr/bin/env python
"""
Script de test du wsgi.py pour vérifier que Django peut être chargé correctement
Cela simule ce que Render fait lors du déploiement
"""

import os
import sys

print("=" * 60)
print("🔍 TEST WSGI - Vérification du chargement Django")
print("=" * 60)

# Affichez le répertoire courant
print(f"\n📁 Current directory: {os.getcwd()}")
print(f"📁 Script directory: {os.path.dirname(os.path.abspath(__file__))}")

# Test 1: Vérifier que les chemins existent
print("\n" + "=" * 60)
print("✓ Test 1: Vérifier les chemins")
print("=" * 60)

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DJANGO_PROJECT_PATH = os.path.join(PROJECT_ROOT, 'louis', 'dblouis')
SETTINGS_PATH = os.path.join(DJANGO_PROJECT_PATH, 'dblouis', 'settings.py')
MANAGE_PATH = os.path.join(DJANGO_PROJECT_PATH, 'manage.py')

print(f"PROJECT_ROOT: {PROJECT_ROOT}")
print(f"  Exists: {'✓' if os.path.exists(PROJECT_ROOT) else '✗'}")

print(f"\nDJANGO_PROJECT_PATH: {DJANGO_PROJECT_PATH}")
print(f"  Exists: {'✓' if os.path.exists(DJANGO_PROJECT_PATH) else '✗'}")

print(f"\nSETTINGS_PATH: {SETTINGS_PATH}")
print(f"  Exists: {'✓' if os.path.exists(SETTINGS_PATH) else '✗'}")

print(f"\nMANAGE_PATH: {MANAGE_PATH}")
print(f"  Exists: {'✓' if os.path.exists(MANAGE_PATH) else '✗'}")

# Test 2: Vérifier que le module peut être importé
print("\n" + "=" * 60)
print("✓ Test 2: Vérifier que le module dblouis peut être importé")
print("=" * 60)

sys.path.insert(0, DJANGO_PROJECT_PATH)
print(f"Added to sys.path: {DJANGO_PROJECT_PATH}")

try:
    import dblouis
    print("✓ Module 'dblouis' imported successfully!")
except ModuleNotFoundError as e:
    print(f"✗ Error importing 'dblouis': {e}")
    sys.exit(1)

# Test 3: Vérifier que Django peut être configuré
print("\n" + "=" * 60)
print("✓ Test 3: Vérifier que Django peut être configuré")
print("=" * 60)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dblouis.settings')
print(f"DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE')}")

try:
    import django
    django.setup()
    print("✓ Django setup successful!")
except Exception as e:
    print(f"✗ Error setting up Django: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Vérifier que l'application WSGI peut être créée
print("\n" + "=" * 60)
print("✓ Test 4: Vérifier que l'application WSGI peut être créée")
print("=" * 60)

try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    print("✓ WSGI application created successfully!")
    print(f"  Application type: {type(application)}")
except Exception as e:
    print(f"✗ Error creating WSGI application: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Success!
print("\n" + "=" * 60)
print("✅ TOUS LES TESTS SONT PASSÉS!")
print("=" * 60)
print("\nVotre configuration WSGI devrait fonctionner correctement sur Render.")
print("Assurez-vous de commit et push vos changements sur GitHub!")
