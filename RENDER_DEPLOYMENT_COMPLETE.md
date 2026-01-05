# 🚀 Guide de Déploiement Complet sur Render

## ✅ Prérequis

- [x] Code Django dans un repository GitHub
- [x] Account Render (gratuit) : https://render.com
- [x] Variables d'environnement configurées

## 📋 Checklist avant déploiement

- [x] Fichier `wsgi.py` configuré correctement (chemins vers Django)
- [x] Fichier `Procfile` avec les bonnes commandes
- [x] Fichier `requirements.txt` à jour
- [x] Fichier `.env.example` avec les variables nécessaires
- [x] Base de données PostgreSQL configurée (optionnel pour Render)

## 🔧 Étapes de déploiement

### Étape 1: Préparer le code local

```bash
# Vérifier que tout est bon localement
cd "C:\Users\louis\OneDrive\Documents\COLLEGE\AUTRE\ENGAGEMENT\CLUBS\CLUB WEB\Django"
python wsgi.py  # Devrait charger sans erreur

# Commit et push
git add wsgi.py Procfile render.yaml RENDER_FIX_SUMMARY.md
git commit -m "Fix Render deployment - corriger wsgi.py path"
git push origin main
```

### Étape 2: Créer un service sur Render

1. Allez sur https://render.com
2. Cliquez sur "New" → "Web Service"
3. Connectez votre repository GitHub
4. Sélectionnez votre repository et branche (`main`)

### Étape 3: Configurer le service

**Paramètres généraux:**
- **Name**: `air-du-vol` (ou votre nom de service)
- **Environment**: `Python 3.13`
- **Build Command**: 
  ```
  pip install -r requirements.txt && cd louis/dblouis && python manage.py collectstatic --no-input && cd ../..
  ```
- **Start Command**: 
  ```
  gunicorn wsgi:application --bind 0.0.0.0:$PORT
  ```

**Variables d'environnement** (à ajouter dans "Environment"):
```
DEBUG=False
DJANGO_SETTINGS_MODULE=dblouis.settings
SECRET_KEY=your-secret-key-here-generate-a-new-one
ALLOWED_HOSTS=your-app.onrender.com,localhost
DATABASE_URL=postgresql://... (si PostgreSQL externe)
```

### Étape 4: Ajouter la base de données (optionnel)

Si vous voulez une base PostgreSQL gérée:
1. Cliquez sur "New" → "PostgreSQL"
2. Donnez-lui un nom
3. Copiez la `DATABASE_URL`
4. Ajoutez-la comme variable d'environnement du service Web

### Étape 5: Déployer

1. Cliquez sur "Deploy"
2. Attendez le déploiement (2-5 minutes)
3. Vérifiez les **Logs** pour des erreurs

## 🐛 Déboggage des erreurs de déploiement

### Erreur: `ModuleNotFoundError: No module named 'dblouis'`
- ✅ **Vérifiez** que `wsgi.py` ajoute bien `louis/dblouis` au `sys.path`
- ✅ **Vérifiez** que le Procfile utilise le bon chemin pour les migrations
- ✅ **Redéployez** après les changements (git push)

### Erreur: `Static files not found`
- ✅ Assurez-vous que `collectstatic` est dans le build command
- ✅ Vérifiez que `STATIC_ROOT` est configuré dans settings.py

### Erreur: `Database connection refused`
- ✅ Vérifiez la `DATABASE_URL`
- ✅ Vérifiez les pare-feu de votre base de données
- ✅ Assurez-vous que les migrations ont été exécutées

### Erreur: `Error loading application`
- ✅ Vérifiez les logs du Render
- ✅ Assurez-vous que Django peut être importé correctement
- ✅ Vérifiez la variable `DJANGO_SETTINGS_MODULE`

## 📊 Vérification après déploiement

1. Allez sur `https://your-app.onrender.com`
2. La page devrait charger sans erreur
3. Vérifiez les logs pour des warnings

```bash
# Voir les logs en direct
# (depuis le dashboard Render, onglet "Logs")
```

## 📝 Notes importantes

⚠️ **PostgreSQL**: La base de données fournie par Render sera supprimée si vous arrêtez le service
⚠️ **Variables d'environnement**: Jamais d'informations sensibles en dur dans le code
⚠️ **Static files**: Assurez-vous qu'ils sont bien collectés lors du build
⚠️ **Migrations**: Elles sont exécutées automatiquement via le `release` command

## 🔗 Ressources utiles

- Docs Render: https://render.com/docs
- Docs Django: https://docs.djangoproject.com/
- Docs Gunicorn: https://docs.gunicorn.org/

## 💡 Si ça n'a pas marché

1. **Vérifiez localement** que tout fonctionne:
   ```bash
   cd louis/dblouis
   python manage.py migrate
   python manage.py collectstatic --no-input
   python manage.py runserver
   ```

2. **Regardez les logs** sur Render (onglet "Logs")

3. **Redéployez manuellement** depuis le dashboard

4. **Contactez le support Render** si le problème persiste

Bonne chance! 🚀
