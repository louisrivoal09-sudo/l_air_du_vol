# Données d'exemple pour tester

## Données prêtes à copier dans l'admin

### Médias - Vidéos

**1. Histoire de l'aviation civile**
```
Titre: Histoire de l'aviation civile
Type: Vidéo
Auteur: L'Air du Vol
Date: 2026-01-02
URL Média: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Description: Un documentary complet sur l'histoire de l'aviation civile depuis les frères Wright jusqu'aux avions modernes.
Image: https://via.placeholder.com/400x240/E63946/FFFFFF?text=Aviation+Civile
```

**2. Le Concorde - Un succès en danger**
```
Titre: Le Concorde - Un succès en danger
Type: Vidéo
Auteur: Aviation Plus
Date: 2025-12-15
URL Média: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Description: Découvrez l'histoire extraordinaire du Concorde, le premier avion de ligne supersonique.
Image: https://via.placeholder.com/400x240/247BA0/FFFFFF?text=Concorde
```

**3. Airbus A380 - Un géant des airs**
```
Titre: Airbus A380 - Un géant des airs
Type: Vidéo
Auteur: Documentary Channel
Date: 2025-11-20
URL Média: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Description: Explorez le plus grand avion de ligne du monde et son impact sur l'industrie aérienne.
Image: https://via.placeholder.com/400x240/F1FAEE/FFFFFF?text=A380
```

### Médias - Podcasts

**1. Podium - L'aviation en questions**
```
Titre: Podium - L'aviation en questions
Type: Podcast
Auteur: Radio Aviation
Date: 2026-01-01
URL Média: https://example.com/podcasts/aviation-questions.mp3
Description: Un podcast hebdomadaire où nous répondons à vos questions sur l'aviation moderne et ses enjeux.
Image: https://via.placeholder.com/400x240/0A2463/FFFFFF?text=Podium
```

**2. Histoires du ciel**
```
Titre: Histoires du ciel
Type: Podcast
Auteur: Pierre Martin
Date: 2025-12-25
URL Média: https://example.com/podcasts/histoires-ciel.mp3
Description: Des histoires fascinantes d'aviateurs et d'innovations aéronautiques à travers les âges.
Image: https://via.placeholder.com/400x240/247BA0/FFFFFF?text=Histoires+Ciel
```

**3. Tech & Aviation**
```
Titre: Tech & Aviation
Type: Podcast
Auteur: Innovation Lab
Date: 2025-12-10
URL Média: https://example.com/podcasts/tech-aviation.mp3
Description: Les dernières technologies qui révolutionnent l'aviation civile et militaire.
Image: https://via.placeholder.com/400x240/F77F00/FFFFFF?text=Tech
```

### Liens - Aviation

**1. FAA - Federal Aviation Administration**
```
Titre: FAA - Federal Aviation Administration
Catégorie: Aviation
URL: https://www.faa.gov
Description: L'agence fédérale américaine responsable de la réglementation et de la sécurité de l'aviation civile.
Image: https://via.placeholder.com/400x240/0A2463/FFFFFF?text=FAA
```

**2. EASA - European Aviation Safety Agency**
```
Titre: EASA - European Aviation Safety Agency
Catégorie: Aviation
URL: https://www.easa.europa.eu
Description: L'autorité européenne de la sécurité aérienne chargée de promouvoir les normes de sécurité.
Image: https://via.placeholder.com/400x240/247BA0/FFFFFF?text=EASA
```

**3. IATA - International Air Transport Association**
```
Titre: IATA - International Air Transport Association
Catégorie: Aviation
URL: https://www.iata.org
Description: L'association internationale représentant les compagnies aériennes du monde entier.
Image: https://via.placeholder.com/400x240/F77F00/FFFFFF?text=IATA
```

### Liens - Ressources

**1. FlightRadar24 - Radar aérien en direct**
```
Titre: FlightRadar24 - Radar aérien en direct
Catégorie: Ressources
URL: https://www.flightradar24.com
Description: Suivez les avions en temps réel sur une carte interactive mondiale.
Image: https://via.placeholder.com/400x240/E63946/FFFFFF?text=FlightRadar24
```

**2. AirliPS - Actualités aéronautiques**
```
Titre: AirliPS - Actualités aéronautiques
Catégorie: Ressources
URL: https://www.airlips.com
Description: Les dernières actualités et innovations du secteur aéronautique.
Image: https://via.placeholder.com/400x240/247BA0/FFFFFF?text=Airlips
```

**3. Wikipedia - Histoire de l'aviation**
```
Titre: Wikipedia - Histoire de l'aviation
Catégorie: Ressources
URL: https://en.wikipedia.org/wiki/History_of_aviation
Description: Une ressource encyclopédique complète sur l'histoire de l'aviation.
Image: https://via.placeholder.com/400x240/0A2463/FFFFFF?text=Wikipedia
```

### Liens - Communauté

**1. Aviation Stack Exchange**
```
Titre: Aviation Stack Exchange
Catégorie: Communauté
URL: https://aviation.stackexchange.com
Description: Un forum communautaire pour poser des questions sur l'aviation.
Image: https://via.placeholder.com/400x240/F77F00/FFFFFF?text=StackExchange
```

**2. Reddit r/aviation**
```
Titre: Reddit r/aviation
Catégorie: Communauté
URL: https://www.reddit.com/r/aviation/
Description: Une communauté active de passionnés d'aviation partageant photos et discussions.
Image: https://via.placeholder.com/400x240/E63946/FFFFFF?text=Reddit
```

### Liens - Outils

**1. Skyvector - Navigation aérienne**
```
Titre: Skyvector - Navigation aérienne
Catégorie: Outils
URL: https://www.skyvector.com
Description: Un outil de planification de vol avec cartes aériennes détaillées.
Image: https://via.placeholder.com/400x240/247BA0/FFFFFF?text=Skyvector
```

**2. Aviation Weather Center**
```
Titre: Aviation Weather Center
Catégorie: Outils
URL: https://www.aviationweather.gov
Description: Les données météorologiques essentielles pour la sécurité aérienne.
Image: https://via.placeholder.com/400x240/0A2463/FFFFFF?text=Weather
```

**3. Aircraft Specifications Database**
```
Titre: Aircraft Specifications Database
Catégorie: Outils
URL: https://www.aircraftdata.com
Description: Une base de données complète des spécifications techniques des avions commerciaux.
Image: https://via.placeholder.com/400x240/F77F00/FFFFFF?text=Specs
```

## Script Python pour ajouter rapidement

```python
# Dans Django Shell: python manage.py shell

from donnelouis.models import Media, Lien
from datetime import date

# Ajouter une vidéo
Media.objects.create(
    titre="Histoire de l'aviation civile",
    type_media="video",
    auteur="L'Air du Vol",
    date_publication=date.today(),
    url_media="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    description="Un documentary complet sur l'histoire de l'aviation civile",
    image_principale="https://via.placeholder.com/400x240/E63946/FFFFFF"
)

# Ajouter un lien
Lien.objects.create(
    titre="FAA - Federal Aviation Administration",
    categorie="aviation",
    url="https://www.faa.gov",
    description="L'agence fédérale américaine responsable de la réglementation de l'aviation civile.",
    image_principale="https://via.placeholder.com/400x240/0A2463/FFFFFF"
)
```

Bonne chance! 🚀
