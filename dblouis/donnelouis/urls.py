from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('articles/', views.liste_articles, name='liste_articles'),
    path('article/<slug:slug>/', views.detail_article, name='detail_article'),
]