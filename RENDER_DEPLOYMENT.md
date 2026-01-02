# 🚀 Déploiement sur Render

Ce guide vous explique comment déployer votre projet Django Club Web sur Render.

## 📋 Prérequis

- Compte GitHub avec votre repository
- Compte Render (gratuit) : https://render.com
- Variables d'environnement configurées

## 📦 Fichiers de configuration

Trois fichiers ont été créés/modifiés pour Render :

1. **render.yaml** - Configuration complète du déploiement
2. **build.sh** - Script de build (migrations, collecte des statics)
3. **start.sh** - Script de démarrage
4. **settings.py** - Configuration Django pour production
5. **.env.example** - Template des variables d'environnement
6. **requirements.txt** - Dépendances Python

## 🔧 Étapes de déploiement

### 1. Préparer le repository

```bash
# Assurez-vous que tous les fichiers sont committés
git add .
git commit -m "Adapter pour Render"
git push
```

### 2. Créer un compte Render

1. Allez sur https://render.com
2. Connectez-vous avec GitHub
3. Autorisez Render à accéder à vos repositories

### 3. Créer une nouvelle Web Service

1. Cliquez sur **New +** → **Web Service**
2. Sélectionnez votre repository
3. Remplissez les paramètres :

| Paramètre | Valeur |
|-----------|--------|
| **Name** | `club-web-django` |
| **Environment** | `Python 3` |
| **Build Command** | `bash build.sh` |
| **Start Command** | `gunicorn dblouis.wsgi:application --bind 0.0.0.0:$PORT` |
| **Plan** | `Free` (ou Premium selon vos besoins) |

### 4. Créer une PostgreSQL Database

1. Allez sur **Databases** → **New +**
2. Créez une PostgreSQL database
3. Configurez :
   - **Name** : `club-web-db`
   - **User** : `clubwebuser`
   - **Plan** : `Free`

### 5. Configurer les variables d'environnement

Sur la page de votre Web Service, allez dans **Environment** et ajoutez :

```env
DEBUG=False
ALLOWED_HOSTS=*.onrender.com
SECRET_KEY=your-secret-key-change-this
```

⚠️ **Important** : Changez `SECRET_KEY` avec une clé sécurisée (Render peut générer automatiquement)

### 6. Connecter la database

Render devrait automatiquement passer `DATABASE_URL` via l'environnement si vous avez lié la database dans render.yaml.

## 🚨 Variables d'environnement

Les principales variables à configurer :

- **DEBUG** : `False` (production)
- **ALLOWED_HOSTS** : `*.onrender.com` ou votre domaine personnalisé
- **SECRET_KEY** : Clé Django sécurisée (génération automatique recommandée)
- **DATABASE_URL** : Générée automatiquement par Render (PostgreSQL)

## 📝 Fichier .env local (développement)

Créez un fichier `.env` à la racine pour le développement local :

```env
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
SECRET_KEY=votre-clé-locale
DATABASE_URL=sqlite:///db.sqlite3
```

## ✅ Vérifier le déploiement

1. Allez sur votre dashboard Render
2. Cliquez sur votre service
3. Vérifiez les logs de build et de démarrage
4. Accédez à votre URL (ex: `club-web-django.onrender.com`)

## 🔗 Domaine personnalisé

Pour ajouter votre domaine :

1. Allez dans **Settings** → **Custom Domain**
2. Entrez votre domaine
3. Configurez les DNS records selon les instructions Render

## 📚 Fichiers importants

- [render.yaml](./render.yaml) - Configuration d'infrastructure
- [build.sh](./build.sh) - Commands de build
- [start.sh](./start.sh) - Commands de démarrage
- [requirements.txt](./requirements.txt) - Dépendances Python
- [settings.py](./louis/dblouis/dblouis/settings.py) - Configuration Django

## 🐛 Troubleshooting

### Le build échoue
- Vérifiez que `render.yaml` est bien à la racine
- Assurez-vous que `build.sh` et `start.sh` sont exécutables
- Vérifiez les logs Render pour les erreurs spécifiques

### Erreur de migration
- Assurez-vous que PostgreSQL est bien créée
- Vérifiez que `DATABASE_URL` est correctement passée
- Les migrations s'exécutent automatiquement dans `build.sh`

### Static files manquants
- WhiteNoise est configuré pour servir les static files
- Les statics sont collectés dans le build (`manage.py collectstatic`)

### Connexion à la database
- Vérifiez que vous avez créé la PostgreSQL database
- Confirmez que Render passe bien la variable `DATABASE_URL`

## 📞 Support

Pour plus d'info : https://docs.render.com/deploy-django
