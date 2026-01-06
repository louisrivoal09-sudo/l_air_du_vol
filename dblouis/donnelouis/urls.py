from django.urls import path
from . import views
from . import views_new_features

urlpatterns = [
    path('', views.index, name='index'),
    path('articles/', views.liste_articles, name='liste_articles'),
    path('article/<slug:slug>/', views.detail_article, name='detail_article'),
    path('catalogue/', views.liste_catalogue, name='liste_catalogue'),
    path('catalogue/<slug:slug>/', views.detail_catalogue, name='detail_catalogue'),
    path('medias/', views.liste_medias, name='liste_medias'),
    path('media/<slug:slug>/', views.detail_media, name='detail_media'),
    path('liens/', views.liste_liens, name='liste_liens'),
    path('contact/', views.contact, name='contact'),
    path('ajouter-article/', views.ajouter_article, name='ajouter_article'),
    path('ajouter-media/', views.ajouter_media, name='ajouter_media'),
    path('ajouter-lien/', views.ajouter_lien, name='ajouter_lien'),
    path('ajouter-avion/', views.ajouter_avion, name='ajouter_avion'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('api/chat/', views.chat_with_ai, name='chat_ai'),
    
    # Forum
    path('forum/', views.forum, name='forum'),
    path('forum/sujet/<path:slug>/', views.detail_sujet_forum, name='detail_sujet_forum'),
    path('forum/creer/', views.creer_sujet_forum, name='creer_sujet_forum'),
    path('forum/editer/<path:slug>/', views.editer_sujet_forum, name='editer_sujet_forum'),
    path('forum/supprimer/<path:slug>/', views.supprimer_sujet_forum, name='supprimer_sujet_forum'),
    path('forum/sujet/<path:sujet_slug>/reponse/<int:reponse_id>/supprimer/', views.supprimer_reponse_forum, name='supprimer_reponse_forum'),
    
    # Profil Utilisateur
    path('profil/', views_new_features.user_profile, name='user_profile'),
    path('api/profil/', views_new_features.get_profile_data, name='get_profile_data'),
    path('api/profil/update/', views_new_features.update_profile, name='update_profile'),
    
    # Commentaires sur articles
    path('api/article/<int:article_id>/comments/', views_new_features.get_article_comments, name='get_comments'),
    path('api/article/<int:article_id>/comment/add/', views_new_features.add_article_comment, name='add_comment'),
    
    # Signalement d'articles
    path('api/article/<int:article_id>/report/', views_new_features.report_article, name='report_article'),
    
    # Articles Favoris
    path('api/article/<int:article_id>/favorite/toggle/', views_new_features.toggle_favorite, name='toggle_favorite'),
    path('api/article/<int:article_id>/favorite/check/', views_new_features.is_favorite, name='is_favorite'),
    path('api/favorites/', views_new_features.get_favorites, name='get_favorites'),
    
    # Mode Offline
    path('api/offline/cache/<int:article_id>/', views_new_features.cache_article, name='cache_article'),
    path('api/offline/cache/', views_new_features.get_offline_cache, name='get_offline_cache'),
    path('api/offline/clear/', views_new_features.clear_offline_cache, name='clear_offline_cache'),
    
    # Notifications en temps réel
    path('api/notifications/', views_new_features.get_notifications, name='get_notifications'),
    path('api/notifications/<int:notif_id>/lue/', views_new_features.marquer_notification_comme_lue, name='marquer_notif_lue'),
    path('api/notifications/marquer-toutes-lues/', views_new_features.marquer_toutes_lues, name='marquer_toutes_lues'),
    
    # Likes/Dislikes - Articles
    path('api/article/<int:article_id>/like/toggle/', views_new_features.toggle_article_like, name='toggle_article_like'),
    
    # Likes/Dislikes - Médias
    path('api/media/<int:media_id>/like/toggle/', views_new_features.toggle_media_like, name='toggle_media_like'),
    
    # Likes/Dislikes - Forum Sujet
    path('api/forum/sujet/<int:sujet_id>/like/toggle/', views_new_features.toggle_forum_sujet_like, name='toggle_forum_sujet_like'),
    
    # Likes/Dislikes - Forum Réponse
    path('api/forum/reponse/<int:reponse_id>/like/toggle/', views_new_features.toggle_forum_reponse_like, name='toggle_forum_reponse_like'),
]

