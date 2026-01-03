# Guide de Déploiement sur Render

## Configuration Render

### Settings à respecter:

1. **Root Directory**: `.` (racine du projet)
2. **Build Command**: `chmod +x build.sh && ./build.sh`
3. **Start Command**: `gunicorn wsgi:application --bind 0.0.0.0:$PORT`

### Checklist de déploiement:

- [ ] Root Directory = `.`
- [ ] Environment variables configurées (DATABASE_URL, SECRET_KEY, etc.)
- [ ] `wsgi.py` correctement configuré avec sys.path
- [ ] `build.sh` exécutable et correct
- [ ] `Procfile` à jour
- [ ] `requirements.txt` complet
- [ ] Tous les fichiers pushés sur GitHub

## Problèmes courants

### ModuleNotFoundError: No module named 'dblouis'

**Cause**: Le sys.path dans wsgi.py n'ajoute pas le bon chemin.

**Solution**:
- Vérifier que le Root Directory est `.`
- Vérifier que `wsgi.py` ajoute `louis` au sys.path
- Vérifier que `DJANGO_SETTINGS_MODULE='dblouis.settings'`

### Build fails

- Vérifier que `build.sh` est exécutable
- Vérifier que les chemins dans `build.sh` sont corrects
- Vérifier que Python packages sont dans `requirements.txt`

## Architecture du projet

```
/
├── wsgi.py                    # Entry point pour Render
├── build.sh                   # Build script
├── Procfile                   # Procédures Render
├── requirements.txt           # Dépendances Python
└── louis/
    └── dblouis/
        ├── manage.py
        ├── db.sqlite3
        ├── dblouis/            # Settings Django
        │   ├── settings.py
        │   ├── urls.py
        │   ├── wsgi.py
        │   └── asgi.py
        └── donnelouis/         # App Django
            ├── models.py
            ├── views.py
            ├── urls.py
            ├── admin.py
            ├── static/
            │   ├── css/
            │   ├── js/
            │   └── images/
            └── templates/
                └── donnelouis/
                    ├── base.html
                    └── ...
```

## Points importants

- **wsgi.py** doit être à la racine du projet (pas dans louis/dblouis)
- **build.sh** navigue vers `louis/dblouis` pour les opérations Django
- **Procfile** appelle `gunicorn wsgi:application`
- Le Root Directory chez Render doit être `.` pour que tous les chemins fonctionnent
