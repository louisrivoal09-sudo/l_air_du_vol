from django.shortcuts import render
from .models import Article

def liste_articles(request):
    articles = Article.objects.all()
    return render(request, 'donnelouis/liste_articles.html', {'articles': articles})
