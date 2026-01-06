# 🧪 Guide de Test du Forum

## 🚀 Démarrage Rapide

### 1. Lancer le serveur Django
```bash
cd c:\Users\louis\OneDrive\Documents\COLLEGE\AUTRE\ENGAGEMENT\CLUBS\CLUB WEB\Django\louis\dblouis
python manage.py runserver
```

### 2. Accéder au forum
Ouvrez votre navigateur à l'adresse:
```
http://localhost:8000/forum/
```

---

## 🧑‍💻 Test en tant que Visiteur (Non Connecté)

### Actions Disponibles
- [ ] Voir la liste de tous les sujets du forum
- [ ] Voir les catégories disponibles
- [ ] Lire les détails d'un sujet
- [ ] Lire les réponses aux sujets
- [ ] Voir le nombre de vues et de réponses

### Points à Vérifier
✅ La page charge correctement
✅ Les sujets s'affichent avec toutes les informations
✅ Le bouton "Se connecter pour poster" s'affiche
✅ Les tags sont affichés correctement
✅ Le filtrage par catégorie fonctionne

---

## 👤 Test Connecté (Utilisateur)

### Données de Connexion
```
Email: admin@example.com
Mot de passe: admin
```

### Actions à Tester
- [ ] Se connecter au site
- [ ] Créer un nouveau sujet
  - [ ] Remplir tous les champs
  - [ ] Sélectionner une catégorie
  - [ ] Ajouter des tags
  - [ ] Soumettre le formulaire
- [ ] Ajouter une réponse à un sujet existant
- [ ] Voir ses contenus dans le forum
- [ ] Éditer un sujet personnel
- [ ] Éditer une réponse personnelle
- [ ] Supprimer un sujet personnel
- [ ] Supprimer une réponse personnelle

### Points à Vérifier - Création de Sujet
- [ ] Le formulaire s'affiche correctement
- [ ] Les champs sont validés
- [ ] Le slug est généré automatiquement
- [ ] La date de création est enregistrée
- [ ] Le sujet apparaît immédiatement dans la liste
- [ ] L'auteur est correct

### Points à Vérifier - Ajout de Réponse
- [ ] Le formulaire s'affiche en bas du sujet
- [ ] La réponse est ajoutée après envoi
- [ ] La date de création est correcte
- [ ] L'auteur est correct
- [ ] Le compteur de réponses augmente

### Points à Vérifier - Édition
- [ ] Seul l'auteur peut éditer son contenu
- [ ] Les données pré-remplissent le formulaire
- [ ] La date de modification change
- [ ] Le contenu est mis à jour correctement

### Points à Vérifier - Suppression
- [ ] La page de confirmation s'affiche
- [ ] Un avertissement est montré
- [ ] Après suppression, redirection vers le forum
- [ ] Le contenu n'existe plus

---

## 🛡️ Test des Permissions

### Test 1: Accès Non Autorisé
```
1. Connecté en tant qu'admin
2. Créer un sujet personnel
3. Ouvrir une session privée (Ctrl+Shift+P)
4. Essayer d'éditer le sujet d'un autre
   → Doit afficher une erreur 403
```

### Test 2: Suppression Non Autorisée
```
1. Connecté en tant qu'utilisateur A
2. Répondre à un sujet
3. Ouvrir une session privée (Ctrl+Shift+P)
4. Essayer de supprimer la réponse de A
   → Doit afficher une erreur 403
```

---

## 📊 Test des Statistiques

- [ ] Le compteur de vues augmente à chaque accès
- [ ] Le nombre de réponses est correct
- [ ] La liste affiche les bonnes statistiques
- [ ] Les dates sont formatées correctement

---

## 🔍 Test du Filtrage

### Test Catégories
- [ ] Filtrer par "Général"
- [ ] Filtrer par "Technique"
- [ ] Filtrer par "Aviation"
- [ ] Filtrer par "Actualités"
- [ ] Afficher tous les sujets

### Vérifications
- [ ] Seuls les sujets de la catégorie s'affichent
- [ ] Le badge de catégorie est correct
- [ ] Le nombre de résultats change

---

## 🎨 Test de l'Interface

### Design
- [ ] La page est responsive (testez sur mobile avec F12)
- [ ] Les boutons sont bien placés
- [ ] Les couleurs sont cohérentes
- [ ] Les icônes s'affichent correctement
- [ ] Les espacements sont bons

### Navigation
- [ ] Le lien "Retour au forum" fonctionne
- [ ] Les breadcrumbs (s'il y en a) sont corrects
- [ ] Les liens internes fonctionnent
- [ ] Les boutons sont cliquables

---

## 🔐 Test de Sécurité

### CSRF Protection
```
1. Ouvrir la console du navigateur (F12)
2. Aller à l'onglet "Network"
3. Envoyer un formulaire
4. Vérifier que le token CSRF est présent
```

### Validation du Formulaire
- [ ] Les champs obligatoires sont validés
- [ ] Les erreurs s'affichent correctement
- [ ] Le formulaire ne s'envoie pas sans données
- [ ] Les messages d'erreur sont clairs

---

## 📝 Test des Données de Test

Les 5 sujets suivants doivent être présents:

1. **"Bienvenue sur le forum L'Air du Vol!"**
   - [ ] Catégorie: Général
   - [ ] Tags: bienvenue, general, communaute
   - [ ] 3 réponses

2. **"Comment fonctionne le forum?"**
   - [ ] Catégorie: Général
   - [ ] Tags: forum, aide, guide

3. **"Question technique: Configuration du serveur"**
   - [ ] Catégorie: Technique
   - [ ] Tags: django, serveur, technique

4. **"Actualité: Les derniers avions commerciaux"**
   - [ ] Catégorie: Actualités
   - [ ] Tags: avions, actualites, commerciaux

5. **"Passionné par l'aviation militaire"**
   - [ ] Catégorie: Aviation
   - [ ] Tags: aviation, militaire, passionnes

---

## 🌐 Test de Compatibilité Navigateur

Testez sur les navigateurs suivants:
- [ ] Chrome/Chromium (Dernière version)
- [ ] Firefox (Dernière version)
- [ ] Safari (Si disponible)
- [ ] Edge (Si disponible)

### Points à Vérifier par Navigateur
- [ ] Les formulaires s'affichent correctement
- [ ] Les boutons sont cliquables
- [ ] L'interface est responsive
- [ ] Pas d'erreurs dans la console

---

## 📱 Test Mobile

Testez sur un téléphone ou simulateur:
- [ ] La navigation est facile au toucher
- [ ] Les boutons ont une taille appropriée
- [ ] Le texte est lisible
- [ ] Les formulaires sont utilisables
- [ ] Pas de défilement horizontal

---

## ⚡ Test de Performance

### Temps de Chargement
```
1. Ouvrir DevTools (F12)
2. Aller à l'onglet "Performance"
3. Charger la page du forum
4. Enregistrer le temps (doit être < 2s)
```

### Nombre de Requêtes
- [ ] Moins de 10 requêtes pour la liste
- [ ] Moins de 5 requêtes supplémentaires pour le détail

---

## 🐛 Rapport de Bugs

Si vous trouvez un problème, notez:

### Format
```
## Bug: [Titre du bug]

### Description
[Description du problème]

### Étapes pour Reproduire
1. ...
2. ...
3. ...

### Résultat Attendu
[Ce qui devrait se passer]

### Résultat Réel
[Ce qui se passe réellement]

### Navigateur
[Navigateur et version]

### Capture d'écran
[Si possible]
```

---

## ✅ Checklist Finale

- [ ] Tous les tests de base passent
- [ ] Les permissions fonctionnent
- [ ] L'interface est responsive
- [ ] Les données de test sont créées
- [ ] Les migrations sont appliquées
- [ ] L'admin Django fonctionne
- [ ] Les messages de succès/erreur s'affichent
- [ ] Les formulaires sont validés
- [ ] Les liens de navigation fonctionnent
- [ ] Pas d'erreurs 500 ou 404

---

## 🎉 Vous avez Terminé!

Si tout passe les tests, votre forum est **prêt en production** ! 🚀
