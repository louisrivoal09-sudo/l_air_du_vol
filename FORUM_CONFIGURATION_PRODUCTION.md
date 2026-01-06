# Configuration Forum - Production Ready

## 🚀 Prêt pour la Production

Ce document contient les configurations recommandées pour déployer le forum en production.

---

## 1️⃣ Variables d'Environnement

Ajoutez ces variables dans votre fichier `.env` ou votre serveur:

```env
# Forum Configuration
FORUM_ENABLE_NOTIFICATIONS=True
FORUM_MODERATE_NEW_TOPICS=False
FORUM_AUTO_APPROVE_REPLIES=True
FORUM_MAX_POSTS_PER_DAY=10
```

---

## 2️⃣ Paramètres Django Recommandés

Dans `settings.py`:

```python
# Pagination
ITEMS_PER_PAGE = 20

# Cache pour les vues populaires
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}

# Session
SESSION_COOKIE_SECURE = True  # HTTPS only
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
```

---

## 3️⃣ Optimisation Base de Données

### Ajouter des Index

Dans `models.py`:

```python
class ForumSujet(models.Model):
    # ... existing fields ...
    
    class Meta:
        ordering = ['-date_creation']
        indexes = [
            models.Index(fields=['categorie', '-date_creation']),
            models.Index(fields=['auteur', '-date_creation']),
            models.Index(fields=['slug']),
        ]
```

Puis créer une migration:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 4️⃣ Modération et Spam

### Ajouter un Champ Modération

```python
class ForumSujet(models.Model):
    # ... existing fields ...
    approuve = models.BooleanField(default=True)
    signale = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-date_creation']
        permissions = [
            ("can_approve_forum_topics", "Peut approuver les sujets"),
            ("can_moderate_forum", "Peut modérer le forum"),
        ]
```

---

## 5️⃣ Notifications par Email

### Configuration SMTP

Dans `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # ou votre serveur SMTP
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-password'
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

### Signal pour Notifications

```python
# Dans signals.py
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ForumReponse

@receiver(post_save, sender=ForumReponse)
def notifier_auteur_sujet(sender, instance, created, **kwargs):
    if created:
        sujet = instance.sujet
        auteur = sujet.auteur
        
        send_mail(
            subject=f'Nouvelle réponse à "{sujet.titre}"',
            message=f'Il y a une nouvelle réponse à votre sujet.\n\n'
                   f'Lire: http://votresite.com/forum/sujet/{sujet.slug}/',
            from_email='noreply@votresite.com',
            recipient_list=[auteur.email],
            fail_silently=True
        )

# Dans apps.py
from django.apps import AppConfig

class DonneLouisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'donnelouis'
    
    def ready(self):
        import donnelouis.signals
```

---

## 6️⃣ Rate Limiting

### Limiter les Requêtes

```python
# Dans settings.py
RATELIMIT_ENABLE = True
RATELIMIT_USE_CACHE = 'default'

# Dans views.py
from django_ratelimit.decorators import ratelimit

@ratelimit(key='user', rate='10/h', method='POST')
@login_required
def creer_sujet_forum(request):
    # ... existing code ...
```

---

## 7️⃣ Backup Automatique

### Script de Backup

```bash
#!/bin/bash
# backup_forum.sh

BACKUP_DIR="/backups/forum"
DATE=$(date +%Y%m%d_%H%M%S)

# Exporter les données
python manage.py dumpdata donnelouis.ForumSujet donnelouis.ForumReponse > \
    $BACKUP_DIR/forum_backup_$DATE.json

# Compresser
gzip $BACKUP_DIR/forum_backup_$DATE.json

# Garder seulement les 30 derniers jours
find $BACKUP_DIR -name "forum_backup_*.json.gz" -mtime +30 -delete

echo "Backup forum complété: forum_backup_$DATE.json.gz"
```

Ajouter à crontab:
```bash
0 2 * * * /home/user/backup_forum.sh
```

---

## 8️⃣ Monitoring

### Logs

```python
# settings.py
LOGGING = {
    'version': 1,
    'handlers': {
        'forum_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/forum.log',
        },
    },
    'loggers': {
        'donnelouis.forum': {
            'handlers': ['forum_file'],
            'level': 'INFO',
        },
    },
}
```

### Logging dans les views

```python
import logging
logger = logging.getLogger(__name__)

def creer_sujet_forum(request):
    logger.info(f"Nouvel sujet créé par {request.user.username}")
    # ... rest of the code ...
```

---

## 9️⃣ Tests Automatisés

### Test Unitaire

```python
# tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from .models import ForumSujet, ForumReponse

class ForumSujetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='12345'
        )
        self.sujet = ForumSujet.objects.create(
            titre='Test Sujet',
            categorie='general',
            auteur=self.user,
            contenu='Test content'
        )
    
    def test_sujet_creation(self):
        self.assertEqual(ForumSujet.objects.count(), 1)
        self.assertEqual(self.sujet.titre, 'Test Sujet')
    
    def test_slug_generation(self):
        self.assertEqual(self.sujet.slug, 'test-sujet')
```

Lancer les tests:
```bash
python manage.py test donnelouis.tests.ForumSujetTestCase
```

---

## 🔟 Checklist Déploiement

- [ ] Backup complet de la base de données
- [ ] Vérifier les permissions des fichiers
- [ ] Configurer les variables d'environnement
- [ ] Tester les migrations
- [ ] Activer le cache Redis
- [ ] Configurer les emails
- [ ] Activer HTTPS/SSL
- [ ] Configurer le rate limiting
- [ ] Mettre en place les logs
- [ ] Tester les notifications
- [ ] Vérifier la sécurité CSRF
- [ ] Tester sur navigateurs principaux
- [ ] Créer une page d'erreur personnalisée
- [ ] Mettre en place un système de monitoring
- [ ] Documenter les procédures de maintenance

---

## 🔐 Sécurité Supplémentaire

### Validation Input

```python
from django import forms
from django.core.exceptions import ValidationError

class ForumSujetForm(forms.ModelForm):
    def clean_titre(self):
        titre = self.cleaned_data.get('titre')
        
        # Vérifier les mots interdits
        forbidden_words = ['spam', 'adult', 'violence']
        if any(word in titre.lower() for word in forbidden_words):
            raise ValidationError("Titre contient des mots interdits")
        
        return titre
    
    def clean_contenu(self):
        contenu = self.cleaned_data.get('contenu')
        
        # Minimum 10 caractères
        if len(contenu) < 10:
            raise ValidationError("Le contenu doit faire au moins 10 caractères")
        
        return contenu
```

---

## 📊 Analytics

### Tracker les Statistiques

```python
class ForumStatistique(models.Model):
    date = models.DateField(auto_now_add=True)
    total_sujets = models.IntegerField()
    total_reponses = models.IntegerField()
    utilisateurs_actifs = models.IntegerField()
    
    class Meta:
        verbose_name_plural = "Statistiques du forum"
```

---

## 🚀 Déploiement Final

```bash
# 1. Collecte des fichiers statiques
python manage.py collectstatic

# 2. Migrations
python manage.py migrate

# 3. Créer un superuser
python manage.py createsuperuser

# 4. Test server
python manage.py runserver 0.0.0.0:8000

# 5. Deployment (avec Gunicorn)
gunicorn dblouis.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

---

## 📚 Ressources Additionnelles

- Django Security: https://docs.djangoproject.com/en/stable/topics/security/
- Django Performance: https://docs.djangoproject.com/en/stable/topics/performance/
- Django Deployment: https://docs.djangoproject.com/en/stable/howto/deployment/

---

## ✅ Conclusion

Votre forum est maintenant **prêt pour la production** avec:
- ✅ Optimisations de performance
- ✅ Sécurité renforcée
- ✅ Monitoring en place
- ✅ Backups automatiques
- ✅ Notifications par email
- ✅ Modération possibles
- ✅ Logs et analytics

**Bon déploiement!** 🚀
