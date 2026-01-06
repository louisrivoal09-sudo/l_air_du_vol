from django.core.management.base import BaseCommand
from django.utils import timezone
from donnelouis.models import ForumSujet, ForumReponse
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Crée des données de test pour le forum'

    def handle(self, *args, **options):
        # Créer un utilisateur de test s'il n'existe pas
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        
        if created:
            user.set_password('admin')
            user.save()
            self.stdout.write(
                self.style.SUCCESS('✓ Utilisateur admin créé (login: admin / password: admin)')
            )
        
        # Créer des sujets de test
        sujets_data = [
            {
                'titre': 'Bienvenue sur le forum L\'Air du Vol!',
                'categorie': 'general',
                'contenu': '''Bonjour et bienvenue sur le forum de la communauté L'Air du Vol!

Cet espace est dédié aux discussions, questions et partages d'expériences autour de l'aviation.

N'hésitez pas à:
- Poser des questions
- Partager vos expériences
- Discuter de l'actualité aéronautique
- Proposer des idées d'améliorations

Bonne visite!''',
                'tags': 'bienvenue, general, communaute',
            },
            {
                'titre': 'Comment fonctionne le forum?',
                'categorie': 'general',
                'contenu': '''Voici quelques informations utiles sur l'utilisation du forum:

1. **Créer un sujet**: Cliquez sur "Créer un sujet" en haut
2. **Répondre**: Remplissez le formulaire en bas de chaque sujet
3. **Éditer/Supprimer**: Vous pouvez modifier vos propres messages
4. **Catégories**: Choisissez la catégorie appropriée pour votre sujet
5. **Tags**: Ajoutez des tags pour faciliter la recherche

Des questions? N'hésitez pas à nous contacter!''',
                'tags': 'forum, aide, guide',
            },
            {
                'titre': 'Question technique: Configuration du serveur',
                'categorie': 'technique',
                'contenu': '''Bonjour,

J'ai des questions concernant la configuration du serveur Django pour ce site.

Quelqu'un pourrait-il m'aider à:
1. Configurer les variables d'environnement
2. Optimiser les performances
3. Sécuriser l'application

Merci d'avance!''',
                'tags': 'django, serveur, technique',
            },
            {
                'titre': 'Actualité: Les derniers avions commerciaux',
                'categorie': 'actualites',
                'contenu': '''Les nouveaux modèles d'avions commerciaux arrivent bientôt!

Quels sont vos avis sur:
- L'Airbus A380
- Le Boeing 787 Dreamliner
- Le Bombardier C Series

Partagez vos impressions et commentaires!''',
                'tags': 'avions, actualites, commerciaux',
            },
            {
                'titre': 'Passionné par l\'aviation militaire',
                'categorie': 'aviation',
                'contenu': '''Bonjour à tous les passionnés d\'aviation militaire!

Créons un espace pour discuter des:
- Avions de chasse (F-16, Rafale, MiG-29...)
- Hélicoptères militaires
- Opérations aériennes
- Histoire de l\'aviation militaire

Venez partager vos connaissances et vos photos!''',
                'tags': 'aviation, militaire, passionnes',
            },
        ]

        for i, sujet_data in enumerate(sujets_data):
            sujet, created = ForumSujet.objects.get_or_create(
                titre=sujet_data['titre'],
                defaults={
                    'slug': sujet_data['titre'].lower().replace(' ', '-').replace('!', '').replace('?', ''),
                    'categorie': sujet_data['categorie'],
                    'auteur': user,
                    'contenu': sujet_data['contenu'],
                    'tags': sujet_data['tags'],
                    'vues': i * 10,  # Nombre de vues croissant
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Sujet créé: {sujet.titre}')
                )
            else:
                self.stdout.write(f'- Sujet existant: {sujet.titre}')

        # Ajouter quelques réponses de test au premier sujet
        if ForumSujet.objects.exists():
            premier_sujet = ForumSujet.objects.first()
            
            reponses_data = [
                'Merci pour cette initiative! J\'attends avec impatience les discussions 🙌',
                'C\'est super! J\'ai beaucoup de questions à poser 🤔',
                'Parfait, je vais partager mes expériences ici 😊',
            ]
            
            for texte in reponses_data:
                reponse, created = ForumReponse.objects.get_or_create(
                    sujet=premier_sujet,
                    contenu=texte,
                    auteur=user,
                )
                
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Réponse ajoutée au sujet "{premier_sujet.titre}"')
                    )

        self.stdout.write(
            self.style.SUCCESS('\n✅ Données de test du forum créées avec succès!')
        )
