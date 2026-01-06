from django.apps import AppConfig


class DonnelouisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'donnelouis'
    
    def ready(self):
        """Active les signaux Django au démarrage de l'application"""
        import donnelouis.signals
