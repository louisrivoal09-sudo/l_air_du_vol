from django.core.management.base import BaseCommand
from donnelouis.models import Article, ImageArticle
from datetime import date

class Command(BaseCommand):
    help = 'Crée des articles de test'

    def handle(self, *args, **kwargs):
        # Article 1: Boeing 737
        article1, created = Article.objects.get_or_create(
            titre="Boeing 737 : le cap des 3000",
            defaults={
                'categorie': 'aviation',
                'date_publication': date(2025, 11, 18),
                'resume': "Le Boeing 737 naît en 1964 alors que Boeing cherche à occuper le marché des court-courriers dominé par le DC-9 et la Caravelle...",
                'image_principale': "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/South_African_Airlink_Boeing_737-200_Advanced_Smith.jpg/500px-South_African_Airlink_Boeing_737-200_Advanced_Smith.jpg",
                'theme1_titre': "Thème I – La genèse du Boeing 737",
                'theme1_section_a_titre': "A. L'apparition du besoin",
                'theme1_section_a_texte': "Au début des années 1960, Boeing prend conscience qu'un segment important du marché aérien lui échappe...",
                'conclusion_titre': "Conclusion",
                'conclusion_texte': "Le Boeing 737 est passé en quelques décennies d'un appareil lancé dans l'incertitude à l'un des avions les plus emblématiques..."
            }
        )
        
        if created:
            # Ajouter des images
            ImageArticle.objects.create(
                article=article1,
                image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/39/Boeing_737_NASA_GPN-2000-001905.jpg/500px-Boeing_737_NASA_GPN-2000-001905.jpg",
                legende="Le prototype du 737",
                ordre=1
            )
            self.stdout.write(self.style.SUCCESS(f'Article "{article1.titre}" créé !'))
        
        # Article 2: F-14 Tomcat
        article2, created = Article.objects.get_or_create(
            titre="Tomcat, félin des mers",
            defaults={
                'categorie': 'avions',
                'date_publication': date(2025, 11, 15),
                'resume': "Le F-14 Tomcat occupe une place unique dans l'histoire de l'aviation militaire...",
                'image_principale': "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f7/US_Navy_051105-F-5480T-005_An_F-14D_Tomcat_conducts_a_mission_over_the_Persian_Gulf-region.jpg/1200px-US_Navy_051105-F-5480T-005_An_F-14D_Tomcat_conducts_a_mission_over_the_Persian_Gulf-region.jpg",
                'theme1_titre': "Thème I – Conception et évolution technique",
                'theme1_section_a_titre': "A. Développement initial",
                'theme1_section_a_texte': "Le F-14A Tomcat s'inscrit dans la continuité d'une longue tradition...",
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Article "{article2.titre}" créé !'))
        
        self.stdout.write(self.style.SUCCESS('✅ Données de test créées avec succès !'))