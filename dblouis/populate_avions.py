#!/usr/bin/env python
"""
Script pour peupler la base de données avec des avions d'exemple
Exécutez avec: python populate_avions.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dblouis.settings')
django.setup()

from donnelouis.models import Avion
from django.contrib.auth.models import User

# Créer l'utilisateur admin s'il n'existe pas
admin_user, _ = User.objects.get_or_create(
    username='admin',
    defaults={'is_staff': True, 'is_superuser': True}
)

# Données d'avions
avions_data = [
    {
        'nom': 'Airbus A380',
        'constructeur': 'Airbus',
        'type_avion': 'Avion de transport',
        'annee_premier_vol': 2007,
        'capacite': 873,
        'description': "L'Airbus A380 est le plus grand avion de ligne du monde. C'est un avion quadrimoteur, conçu et fabriqué par le groupe Airbus en tant que réponse à la croissance du trafic aérien mondial et à la congestion des aéroports majeurs.",
        'image_principale': 'https://images.unsplash.com/photo-1464037866556-6812c9d1c72e?w=800&h=400&fit=crop'
    },
    {
        'nom': 'Boeing 747',
        'constructeur': 'Boeing',
        'type_avion': 'Avion de transport',
        'annee_premier_vol': 1969,
        'capacite': 524,
        'description': "Le Boeing 747 est un avion de ligne géant produit par la société Boeing de 1969 à 2023. C'est le premier jumbo-jet de l'histoire de l'aviation civile, et il a révolutionné le transport aérien international.",
        'image_principale': 'https://images.unsplash.com/photo-1556388208-06f0e1f6e675?w=800&h=400&fit=crop'
    },
    {
        'nom': 'Concorde',
        'constructeur': 'Aérospatiale / BAC',
        'type_avion': 'Avion supersonique',
        'annee_premier_vol': 1969,
        'capacite': 100,
        'description': "Le Concorde est un avion de transport supersonique conçu par une association entre l'Aérospatiale française et la compagnie britannique British Aircraft Corporation (BAC). Il était capable de voler à plus de deux fois la vitesse du son.",
        'image_principale': 'https://images.unsplash.com/photo-1518639802208-1f5f17e5f06d?w=800&h=400&fit=crop'
    },
    {
        'nom': 'De Havilland Comet',
        'constructeur': 'De Havilland',
        'type_avion': 'Avion de transport',
        'annee_premier_vol': 1949,
        'capacite': 36,
        'description': "Le De Havilland Comet est un avion de ligne pionnier avec quatre moteurs à réaction. C'était le premier avion commercial à réaction jamais utilisé en service régulier, inaugurant la période des avions à réaction en aviation civile.",
        'image_principale': 'https://images.unsplash.com/photo-1569344292200-3954b2490b0b?w=800&h=400&fit=crop'
    },
    {
        'nom': 'Airbus A350',
        'constructeur': 'Airbus',
        'type_avion': 'Avion de transport',
        'annee_premier_vol': 2013,
        'capacite': 325,
        'description': "L'Airbus A350 est un avion de ligne long-courrier conçu et fabriqué par le groupe Airbus. C'est un biréacteur à large fuselage destiné à concurrencer le Boeing 777 et 787 Dreamliner.",
        'image_principale': 'https://images.unsplash.com/photo-1565149533153-f4d81f86a1b1?w=800&h=400&fit=crop'
    },
    {
        'nom': 'Boeing 787 Dreamliner',
        'constructeur': 'Boeing',
        'type_avion': 'Avion de transport',
        'annee_premier_vol': 2009,
        'capacite': 290,
        'description': "Le Boeing 787 Dreamliner est un avion de ligne long-courrier, biréacteur à large fuselage. Il représente une nouvelle génération d'avions commerciaux plus efficaces en consommation de carburant et dotés d'un confort accru.",
        'image_principale': 'https://images.unsplash.com/photo-1581092162562-40038f70cdf4?w=800&h=400&fit=crop'
    },
    {
        'nom': 'Cessna 172',
        'constructeur': 'Cessna',
        'type_avion': 'Avion léger',
        'annee_premier_vol': 1955,
        'capacite': 4,
        'description': "Le Cessna 172 est un avion léger et utilitaire produit par Cessna depuis 1955. C'est l'un des avions les plus populaires au monde avec plus de 44 000 exemplaires construits. Il est très apprécié pour la formation et les vols de loisir.",
        'image_principale': 'https://images.unsplash.com/photo-1570359677326-e75a4a5de595?w=800&h=400&fit=crop'
    },
    {
        'nom': 'Airbus A320',
        'constructeur': 'Airbus',
        'type_avion': 'Avion de transport',
        'annee_premier_vol': 1987,
        'capacite': 194,
        'description': "L'Airbus A320 est un avion de ligne court et moyen-courrier. C'est l'un des avions commerciaux les plus vendus au monde, et il est utilisé par des centaines de compagnies aériennes.",
        'image_principale': 'https://images.unsplash.com/photo-1495521821757-a1efb6729352?w=800&h=400&fit=crop'
    }
]

# Créer les avions
created_count = 0
for avion_data in avions_data:
    avion, created = Avion.objects.get_or_create(
        nom=avion_data['nom'],
        defaults=avion_data
    )
    if created:
        created_count += 1
        print(f"✅ Avion créé: {avion.nom}")
    else:
        print(f"⏭️  Avion existant: {avion.nom}")

print(f"\n🎉 {created_count} avion(s) créé(s) avec succès!")
print(f"Total avions: {Avion.objects.count()}")
