from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from .models import Article

def index(request):
    """Page d'accueil"""
    articles_recents = Article.objects.all()[:3]
    total_articles = Article.objects.count()
    
    context = {
        'articles_recents': articles_recents,
        'stats': {
            'total_articles': total_articles,
        }
    }
    return render(request, 'donnelouis/index.html', context)


def liste_articles(request):
    """Liste de tous les articles avec filtres"""
    articles = Article.objects.all()
    
    # Statistiques par catégorie
    stats = {
        'aviation': Article.objects.filter(categorie='aviation').count(),
        'avions': Article.objects.filter(categorie='avions').count(),
        'operations': Article.objects.filter(categorie='operations').count(),
    }
    
    context = {
        'articles': articles,
        'stats': stats,
    }
    return render(request, 'donnelouis/liste_articles.html', context)


def detail_article(request, slug):
    """Détail d'un article"""
    article = get_object_or_404(Article, slug=slug)
    
    context = {
        'article': article,
    }
    return render(request, 'donnelouis/detail_article.html', context)