# Guide complet - Médias et Liens dans Django

## 📚 Vue d'ensemble

Vous avez maintenant 3 sections dans votre application :
1. **Articles** - Contenu texte détaillé
2. **Médias** - Vidéos et Podcasts
3. **Liens** - Ressources externes

## 🔧 Comment ça marche ?

### Étape 1 : Appliquer les migrations

Ouvrez un terminal dans le répertoire `dblouis/` :

```bash
python manage.py migrate
```

Cela créera les tables nécessaires dans la base de données.

---

## 📺 MÉDIAS (Vidéos & Podcasts)

### 1. Ajouter un média dans l'admin Django

1. Allez sur http://localhost:8000/admin/
2. Connectez-vous avec votre compte administrateur
3. Cliquez sur **"Médias"** dans la section **Donnelouis**
4. Cliquez sur **"Ajouter un média"**

### 2. Remplir les champs

#### **Informations de base**
- **Titre** : Le nom du média (ex: "Histoire de l'aviation")
- **Slug** : Auto-généré à partir du titre
- **Type de média** : Choisir entre "Vidéo" ou "Podcast"
- **Auteur** : Qui a créé le contenu (par défaut: "L'Air du Vol")
- **Date de publication** : La date du média

#### **Contenu**
- **Description** : Résumé du contenu
- **URL du média** : 
  - Pour **YouTube** : Collez l'URL complète (ex: https://www.youtube.com/watch?v=VIDEO_ID)
  - Pour **Dailymotion** : L'URL complète
  - Pour **MP3/Audio** : L'URL du fichier audio direct
- **Image principale** : URL d'une image/couverture (optionnel)

### 3. Exemples d'URLs

**Vidéo YouTube :**
```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

**Podcast MP3 :**
```
https://example.com/podcast/episode1.mp3
```

**Vidéo MP4 direct :**
```
https://example.com/videos/aviation.mp4
```

### 4. Accéder à la page

- **Liste** : http://localhost:8000/medias/
- **Détail** : http://localhost:8000/media/mon-media/

---

## 🔗 LIENS (Ressources externes)

### 1. Ajouter un lien dans l'admin Django

1. Allez sur http://localhost:8000/admin/
2. Cliquez sur **"Liens"** dans la section **Donnelouis**
3. Cliquez sur **"Ajouter un lien"**

### 2. Remplir les champs

#### **Informations de base**
- **Titre** : Le nom du site/ressource (ex: "FAA - Federal Aviation Administration")
- **Slug** : Auto-généré
- **Catégorie** : Choisir entre :
  - Aviation
  - Ressources
  - Communauté
  - Outils

#### **Contenu**
- **Description** : Explication du lien
- **URL** : L'adresse complète (ex: https://www.faa.gov)
- **Image principale** : Logo ou capture du site (optionnel)

### 3. Exemples

```
Titre: FAA
Catégorie: Aviation
URL: https://www.faa.gov
Description: L'agence fédérale américaine de l'aviation civile
```

### 4. Accéder à la page

- **Liste** : http://localhost:8000/liens/

---

## 🎯 Fonctionnalités des pages

### Filtrage
- Cliquez sur les catégories pour filtrer
- Utilisez la barre de recherche pour trouver du contenu

### Tri
- Triez par date, alphabétique, etc.

### Navigation
- Cliquez sur une carte pour voir les détails
- Les médias s'ouvrent avec un lecteur vidéo/audio intégré
- Les liens s'ouvrent directement dans une nouvelle fenêtre

---

## 🧠 Comment ça fonctionne en arrière-plan

### Modèles Django

**Media (Média)**
- `titre` : Nom du contenu
- `slug` : URL friendly (auto-généré)
- `type_media` : video ou podcast
- `description` : Texte descriptif
- `url_media` : Lien vers le contenu
- `image_principale` : Couverture
- `date_publication` : Date de publication
- `auteur` : Créateur du contenu

**Lien (Liens)**
- `titre` : Nom du lien
- `slug` : URL friendly
- `categorie` : Aviation/Ressources/Communauté/Outils
- `description` : Explication du lien
- `url` : Adresse du site
- `image_principale` : Image/logo

### Fichiers modifiés/créés

**Backend :**
- `models.py` - Ajout des modèles Media et Lien
- `admin.py` - Interface d'administration
- `views.py` - Fonctions pour afficher les pages
- `urls.py` - Routes des pages
- `migrations/0002_media_lien.py` - Migration de base de données

**Frontend :**
- `templates/donnelouis/liste_medias.html` - Page liste des médias
- `templates/donnelouis/detail_media.html` - Page détail d'un média
- `templates/donnelouis/liste_liens.html` - Page liste des liens

---

## ⚡ Commandes utiles

```bash
# Voir les migrations
python manage.py showmigrations

# Appliquer les migrations
python manage.py migrate

# Créer un superuser (administrateur)
python manage.py createsuperuser

# Lancer le serveur
python manage.py runserver

# Accéder à l'admin
# http://localhost:8000/admin/
```

---

## 🎨 Personnalisation

### Changer les catégories de liens

Éditez `models.py` :
```python
CATEGORIES = [
    ('aviation', 'Aviation'),
    ('ressources', 'Ressources'),
    ('communaute', 'Communauté'),
    ('outils', 'Outils'),
    # Ajoutez vos propres catégories ici
]
```

### Modifier le design

Les CSS se trouvent dans les templates (dans la balise `<style>`)

---

## 🚀 Prochaines étapes

1. **Appliquer la migration** : `python manage.py migrate`
2. **Aller à l'admin** : http://localhost:8000/admin/
3. **Ajouter du contenu** : Médias et Liens
4. **Vérifier les pages** : Vérifier que tout s'affiche correctement

---

## ❓ Questions fréquentes

**Q: Mes vidéos YouTube ne s'affichent pas ?**
A: Vérifiez que vous utilisez l'URL complète avec le video ID.

**Q: Comment changer les couleurs ?**
A: Modifiez les CSS dans les templates (`.media-card`, `.lien-card`, etc.)

**Q: Puis-je avoir plusieurs images pour un média ?**
A: Oui, créez un modèle `ImageMedia` similaire à `ImageArticle` et ajoutez-le comme inlined admin.

**Q: Comment supprimer un média/lien ?**
A: Allez dans l'admin, cliquez sur le média/lien, puis cliquez "Supprimer".
