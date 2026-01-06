# Middleware pour gérer les limitations d'accès pour utilisateurs non connectés

from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from datetime import datetime


class AccessLimitationMiddleware(MiddlewareMixin):
    """
    Middleware pour tracker l'accès aux contenus (articles, médias)
    et limiter les utilisateurs non connectés à 10 contenus par jour
    """
    
    def process_request(self, request):
        # Initialiser la session si nécessaire
        if 'article_views' not in request.session:
            request.session['article_views'] = []
        
        # Ajouter des informations contextuelles
        if not request.user.is_authenticated:
            today = datetime.now().date().isoformat()
            views = request.session.get('article_views', [])
            views_today = [v for v in views if v.startswith(today)]
            
            request.article_views_today = len(views_today)
            request.article_remaining = max(0, 10 - len(views_today))
        else:
            request.article_views_today = 0
            request.article_remaining = None
        
        return None
