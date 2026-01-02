# Résumé rapide - 3 minutes pour démarrer

## ✅ 1. Appliquer les migrations (Une seule fois)

```bash
cd dblouis
python manage.py migrate
```

## 👤 2. Créer un compte admin (Une seule fois)

```bash
python manage.py createsuperuser
```

## 🚀 3. Lancer le serveur

```bash
python manage.py runserver
```

Accédez à http://localhost:8000/admin/

## 📊 Structure créée

### Modèles
```
Article  ✓ (existant)
├── Vidéo & Podcast
├── Liens

Media
├── titre
├── type_media (video/podcast)
├── url_media (YouTube, MP3, etc)
├── description
└── image_principale

Lien
├── titre
├── categorie (aviation/ressources/communaute/outils)
├── url
├── description
└── image_principale
```

### Pages
```
/articles/              → Liste des articles
/article/<slug>/        → Détail article
/medias/                → Liste médias
/media/<slug>/          → Lecteur vidéo/podcast
/liens/                 → Liste des liens (cliquable)
```

## 🎯 Ajouter du contenu

### Ajouter un média
1. Admin > Médias > Ajouter un média
2. Remplir titre, type (video/podcast), url_media
3. Pour YouTube: `https://www.youtube.com/watch?v=ID`
4. Pour MP3: `https://example.com/file.mp3`

### Ajouter un lien
1. Admin > Liens > Ajouter un lien
2. Remplir titre, catégorie, url, description
3. L'image est optionnelle

## 💾 Fichiers modifiés

```
models.py          → Ajout Media + Lien
admin.py           → Admin interface
views.py           → 2 nouvelles vues (liste_medias, detail_media, liste_liens)
urls.py            → 3 nouvelles routes
migrations/0002... → Création des tables
templates/
├── liste_medias.html      → Page grille des médias
├── detail_media.html      → Lecteur intégré
└── liste_liens.html       → Page grille des liens
```

## 🔧 Structure des templates

Tous les templates ont:
- **Recherche** ✓
- **Filtrage par catégorie** ✓
- **Tri** ✓
- **Design responsive** ✓
- **Lecteur vidéo intégré** ✓ (médias)

## ⚡ Commandes rapides

```bash
# Voir la liste des médias depuis Django
python manage.py shell
>>> from donnelouis.models import Media
>>> Media.objects.all()

# Créer un média via shell
>>> Media.objects.create(
...     titre="Test",
...     type_media="video",
...     url_media="https://www.youtube.com/watch?v=...",
...     description="Description",
...     date_publication="2026-01-02"
... )
```

## 🎨 Personnaliser

- **Couleurs**: Modifiez les CSS dans les templates (`.media-card`, etc)
- **Catégories**: Éditez `CATEGORIES` dans `models.py`
- **Ordre d'affichage**: Modifiez `ordering` dans les Meta classes

## 📱 Design

- ✓ Responsive (mobile/tablet/desktop)
- ✓ Grille dynamique
- ✓ Filtres interactifs
- ✓ Lecteur vidéo/audio intégré
- ✓ Liens qui ouvrent en nouvel onglet

C'est tout ! 🎉
