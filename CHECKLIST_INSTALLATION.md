# ✅ Checklist d'installation

## Avant de commencer
- [ ] Django est installé
- [ ] Python 3.8+ est installé
- [ ] Vous êtes dans le répertoire `dblouis/`
- [ ] L'environnement virtuel est activé

---

## Étape 1: Appliquer les migrations

```bash
cd dblouis
python manage.py migrate
```

**Résultat attendu:**
```
Running migrations:
  Applying donnelouis.0002_media_lien... OK
```

Si vous avez cette erreur:
```
No changes detected in app 'donnelouis'
```

C'est normal! Les migrations pourraient déjà être appliquées.

---

## Étape 2: Créer un compte administrateur (si pas encore fait)

```bash
python manage.py createsuperuser
```

Suivez les instructions (username, email, password)

---

## Étape 3: Lancer le serveur

```bash
python manage.py runserver
```

Vous devriez voir:
```
Starting development server at http://127.0.0.1:8000/
```

---

## Étape 4: Accéder à l'admin

Ouvrez dans votre navigateur:
```
http://localhost:8000/admin/
```

Connectez-vous avec vos identifiants.

---

## Étape 5: Vérifier les modèles

Dans l'admin, vous devriez voir:

✅ **Donnelouis** (section)
   - Articles ✓ (existant)
   - Articles d'images ✓ (existant)
   - **Médias** ✨ (nouveau)
   - **Liens** ✨ (nouveau)

---

## Étape 6: Ajouter du contenu

### Option A: Via l'interface admin

**Pour ajouter un Média:**
1. Cliquez sur "Médias"
2. Cliquez sur "+ Ajouter un média"
3. Remplissez le formulaire (voir EXEMPLES_DONNEES.md)
4. Cliquez sur "Enregistrer"

**Pour ajouter un Lien:**
1. Cliquez sur "Liens"
2. Cliquez sur "+ Ajouter un lien"
3. Remplissez le formulaire (voir EXEMPLES_DONNEES.md)
4. Cliquez sur "Enregistrer"

### Option B: Via le shell Django

```bash
python manage.py shell
```

```python
from donnelouis.models import Media, Lien
from datetime import date

# Ajouter une vidéo
Media.objects.create(
    titre="Ma première vidéo",
    type_media="video",
    url_media="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    description="Une super vidéo",
    date_publication=date.today(),
    auteur="Mon Nom"
)

# Ajouter un lien
Lien.objects.create(
    titre="Google",
    url="https://www.google.com",
    categorie="ressources",
    description="Moteur de recherche populaire"
)

# Vérifier
print(Media.objects.all())
print(Lien.objects.all())

# Quitter
exit()
```

---

## Étape 7: Vérifier les pages

Dans votre navigateur:

### Page d'accueil
```
http://localhost:8000/
```
Vous devriez voir 3 cartes: Articles, Médias, Liens

### Page liste des médias
```
http://localhost:8000/medias/
```
Filtres: Vidéos/Podcasts

### Page détail d'un média
```
http://localhost:8000/media/slug-du-media/
```
Devrait afficher le lecteur vidéo/audio

### Page liste des liens
```
http://localhost:8000/liens/
```
Filtres: 4 catégories

---

## ✅ Problèmes courants

### ❌ "ModuleNotFoundError: No module named 'django'"
```bash
pip install django
```

### ❌ "No such table: donnelouis_media"
```bash
python manage.py migrate
```

### ❌ "The database is locked"
```
- Fermez tous les autres processus
- Supprimez db.sqlite3 et relancez migrate
```

### ❌ Les vidéos YouTube ne s'affichent pas
- Vérifiez que l'URL est complète avec l'ID
- Exemple: `https://www.youtube.com/watch?v=XXXXX`
- Pas `https://youtu.be/XXXXX`

### ❌ Les liens ne s'ouvrent pas
- Vérifiez que l'URL commence par `http://` ou `https://`
- Les URL doivent être complètes

### ❌ Le slug ne se génère pas automatiquement
- Cliquez sur le champ slug une fois que vous avez entré un titre
- Il devrait se remplir automatiquement

---

## 📊 Vérification du contenu

```python
# Depuis le shell Django
python manage.py shell

from donnelouis.models import Media, Lien

# Compter les éléments
print(f"Médias: {Media.objects.count()}")
print(f"Liens: {Lien.objects.count()}")

# Lister les médias
for media in Media.objects.all():
    print(f"- {media.titre} ({media.type_media})")

# Lister les liens
for lien in Lien.objects.all():
    print(f"- {lien.titre} ({lien.categorie})")
```

---

## 🎯 Ordre d'affichage

Les éléments s'affichent dans cet ordre:
- **Médias**: Plus récents d'abord (par date_publication)
- **Liens**: Par catégorie, puis alphabétiquement

---

## 🎨 Personnalisation

Vous pouvez modifier:

1. **Couleurs**: CSS dans les templates
2. **Catégories de liens**: `CATEGORIES` dans `models.py`
3. **Nombre de colonnes**: CSS `.grid` dans templates
4. **Ordre de tri**: `ordering` dans les `Meta` classes

---

## 📚 Documentation

Consultez:
- `DEMARRAGE_RAPIDE.md` - 3 minutes pour démarrer
- `GUIDE_MEDIAS_LIENS.md` - Guide complet détaillé
- `EXEMPLES_DONNEES.md` - Données prêtes à copier
- `ARCHITECTURE.md` - Vue d'ensemble technique
- `RESUME_MODIFICATIONS.md` - Tout ce qui a changé

---

## 🚀 Vous êtes prêt!

Une fois tout coche:
1. Le serveur fonctionne
2. L'admin est accessible
3. Les pages affichent le contenu
4. Les filtres et tri fonctionnent

Vous pouvez commencer à ajouter du contenu! 🎉

---

## 💡 Tips utiles

- Utilisez placeholder.com pour les images de test
- Testez avec les URLs YouTube de test (voir EXEMPLES_DONNEES.md)
- Les modifications en admin s'affichent immédiatement sur le site
- Vous pouvez supprimer un élément en allant dans son détail et en cliquant "Supprimer"

---

## 📞 Besoin d'aide?

1. Consultez les documentations fournies
2. Vérifiez que tous les fichiers sont en place
3. Relancez `python manage.py migrate`
4. Vérifiez que le serveur Django est actif

Bonne chance! 🚀
