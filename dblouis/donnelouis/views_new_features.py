"""
Vues pour les nouvelles fonctionnalités:
- Commentaires sur articles
- Signalements
- Articles favoris
- Galerie d'avions
- Profil utilisateur
- Mode offline
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from .models import (
    Article, ArticleComment, ArticleReport, FavoriteArticle,
    Avion, UserProfile, OfflineCache
)


# ============================================================================
# COMMENTAIRES SUR ARTICLES
# ============================================================================

@require_http_methods(["POST"])
def add_article_comment(request, article_id):
    """Ajouter un commentaire sur un article"""
    try:
        article = Article.objects.get(id=article_id)
        data = json.loads(request.body)
        
        comment = ArticleComment.objects.create(
            article=article,
            auteur=request.user if request.user.is_authenticated else None,
            auteur_nom=data.get('auteur_nom', ''),
            auteur_email=data.get('auteur_email', ''),
            contenu=data.get('contenu', ''),
            approuve=True  # Les commentaires sont approuvés directement
        )
        
        # Créer une notification pour l'auteur de l'article
        from .models import Notification
        if article.auteur:  # Si c'est enregistré comme ForeignKey
            auteurs = Article.objects.filter(id=article_id)
            for auteur in auteurs:
                if hasattr(auteur, 'user'):
                    Notification.objects.create(
                        utilisateur=auteur.user,
                        type_notif='commentaire_reponse',
                        titre=f"💭 Nouveau commentaire sur {article.titre}",
                        message=f"{comment.get_auteur_display()} a commenté votre article",
                        article=article
                    )
        
        return JsonResponse({
            'success': True,
            'comment_id': comment.id,
            'message': 'Commentaire publié avec succès !'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_http_methods(["GET"])
def get_article_comments(request, article_id):
    """Récupérer les commentaires d'un article"""
    try:
        article = Article.objects.get(id=article_id)
        comments = ArticleComment.objects.filter(article=article, approuve=True).select_related('auteur')
        
        data = [
            {
                'id': c.id,
                'auteur': c.get_auteur_display(),
                'contenu': c.contenu,
                'date': c.date_creation.strftime('%d/%m/%Y %H:%M'),
            }
            for c in comments
        ]
        
        return JsonResponse({'success': True, 'comments': data})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


# ============================================================================
# SIGNALEMENTS
# ============================================================================

@require_http_methods(["POST"])
def report_article(request, article_id):
    """Signaler un article inapproprié"""
    try:
        article = Article.objects.get(id=article_id)
        data = json.loads(request.body)
        
        report = ArticleReport.objects.create(
            article=article,
            signaleur=request.user if request.user.is_authenticated else None,
            raison=data.get('raison', 'autre'),
            description=data.get('description', '')
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Merci! Nous traiterons votre signalement rapidement.'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


# ============================================================================
# ARTICLES FAVORIS
# ============================================================================

@login_required
@require_http_methods(["POST"])
def toggle_favorite(request, article_id):
    """Ajouter/retirer un article des favoris"""
    try:
        article = Article.objects.get(id=article_id)
        favorite, created = FavoriteArticle.objects.get_or_create(
            user=request.user,
            article=article
        )
        
        if not created:
            # Supprimer si déjà en favori
            favorite.delete()
            return JsonResponse({
                'success': True,
                'is_favorite': False,
                'message': 'Retiré des favoris'
            })
        else:
            # Ajouter aux favoris
            return JsonResponse({
                'success': True,
                'is_favorite': True,
                'message': 'Ajouté aux favoris'
            })
    except Article.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Article non trouvé'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
def is_favorite(request, article_id):
    """Vérifier si un article est en favori"""
    try:
        article = Article.objects.get(id=article_id)
        is_fav = FavoriteArticle.objects.filter(
            user=request.user,
            article=article
        ).exists()
        return JsonResponse({'is_favorite': is_fav})
    except:
        return JsonResponse({'is_favorite': False})


@login_required
def get_favorites(request):
    """Récupérer tous les articles favoris de l'utilisateur"""
    favorites = FavoriteArticle.objects.filter(user=request.user).select_related('article')
    data = [
        {
            'id': f.article.id,
            'titre': f.article.titre,
            'slug': f.article.slug,
            'resume': f.article.resume,
            'image': f.article.image_principale,
            'date_ajout': f.date_ajout.strftime('%d/%m/%Y')
        }
        for f in favorites
    ]
    return JsonResponse({'favorites': data})


# ============================================================================
# PROFIL UTILISATEUR
# ============================================================================

@login_required
def user_profile(request):
    """Page de profil utilisateur"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    favorites = FavoriteArticle.objects.filter(user=request.user).count()
    comments = ArticleComment.objects.filter(auteur=request.user).count()
    
    context = {
        'profile': profile,
        'user': request.user,
        'nombre_favoris': favorites,
        'nombre_commentaires': comments,
    }
    return render(request, 'donnelouis/profil.html', context)


@login_required
@require_http_methods(["POST"])
def update_profile(request):
    """Mettre à jour le profil utilisateur"""
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        data = json.loads(request.body)
        
        if 'bio' in data:
            profile.bio = data['bio']
        if 'avatar_url' in data:
            profile.avatar_url = data['avatar_url']
        
        profile.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Profil mis à jour'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
def get_profile_data(request):
    """API: Données du profil en JSON"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    data = {
        'username': request.user.username,
        'email': request.user.email,
        'bio': profile.bio,
        'avatar_url': profile.avatar_url,
        'nombre_articles_lus': profile.nombre_articles_lus,
        'nombre_posts_forum': profile.nombre_posts_forum,
        'nombre_commentaires': profile.nombre_commentaires,
        'date_inscription': request.user.date_joined.strftime('%d/%m/%Y'),
    }
    return JsonResponse(data)


# ============================================================================
# MODE OFFLINE
# ============================================================================

@login_required
@require_http_methods(["POST"])
def cache_article(request, article_id):
    """Mettre en cache un article pour le mode offline"""
    try:
        article = Article.objects.get(id=article_id)
        cache, created = OfflineCache.objects.get_or_create(
            user=request.user,
            article=article
        )
        return JsonResponse({
            'success': True,
            'cached': created,
            'message': 'Article mis en cache pour le mode offline'
        })
    except:
        return JsonResponse({'success': False, 'error': 'Erreur lors du cache'}, status=400)


@login_required
def get_offline_cache(request):
    """Récupérer tous les articles en cache pour l'utilisateur"""
    cached_items = OfflineCache.objects.filter(user=request.user).select_related(
        'article', 'avion', 'media'
    )
    
    data = []
    for item in cached_items:
        if item.article:
            data.append({
                'type': 'article',
                'id': item.article.id,
                'titre': item.article.titre,
                'slug': item.article.slug,
                'resume': item.article.resume,
                'image': item.article.image_principale,
            })
        elif item.avion:
            data.append({
                'type': 'avion',
                'id': item.avion.id,
                'nom': item.avion.nom,
                'slug': item.avion.slug,
                'description': item.avion.description,
                'image': item.avion.image_principale,
            })
        elif item.media:
            data.append({
                'type': 'media',
                'id': item.media.id,
                'titre': item.media.titre,
                'slug': item.media.slug,
                'description': item.media.description,
                'image': item.media.image_principale,
            })
    
    return JsonResponse({'cached_items': data})


@login_required
@require_http_methods(["POST"])
def clear_offline_cache(request):
    """Vider le cache offline"""
    try:
        OfflineCache.objects.filter(user=request.user).delete()
        return JsonResponse({'success': True, 'message': 'Cache vidé'})
    except:
        return JsonResponse({'success': False, 'error': 'Erreur lors du vidage'}, status=400)


# ============================================================================
# NOTIFICATIONS EN TEMPS RÉEL
# ============================================================================

from .models import Notification, CommentNotification

@login_required
@require_http_methods(["GET"])
def get_notifications(request):
    """API: Récupérer les notifications non lues de l'utilisateur"""
    notifications = Notification.objects.filter(
        utilisateur=request.user,
        lue=False
    ).order_by('-date_creation')[:20]
    
    data = [
        {
            'id': n.id,
            'type': n.type_notif,
            'titre': n.titre,
            'message': n.message,
            'date': n.date_creation.strftime('%d/%m/%Y %H:%M'),
            'url': get_notification_url(n),
        }
        for n in notifications
    ]
    
    return JsonResponse({
        'success': True,
        'notifications': data,
        'count': len(data)
    })


@login_required
@require_http_methods(["POST"])
def marquer_notification_comme_lue(request, notif_id):
    """Marquer une notification comme lue"""
    try:
        notif = Notification.objects.get(id=notif_id, utilisateur=request.user)
        notif.marquer_comme_lue()
        return JsonResponse({'success': True})
    except:
        return JsonResponse({'success': False, 'error': 'Notification non trouvée'}, status=404)


@login_required
@require_http_methods(["POST"])
def marquer_toutes_lues(request):
    """Marquer toutes les notifications comme lues"""
    Notification.objects.filter(utilisateur=request.user, lue=False).update(lue=True)
    return JsonResponse({'success': True})


def get_notification_url(notification):
    """Récupérer l'URL correspondant à la notification"""
    if notification.article:
        return f"/article/{notification.article.slug}/"
    elif notification.sujet_forum:
        return f"/forum/sujet/{notification.sujet_forum.slug}/"
    elif notification.media:
        return f"/media/{notification.media.slug}/"
    return "/"


# Utilisateurs NON connectés - Notifications d'incitation à l'inscription
def create_auth_notifications(request):
    """Créer des notifications pour encourager l'inscription"""
    session_key = request.session.session_key
    
    # Ne pas créer si l'utilisateur est connecté
    if request.user.is_authenticated:
        return
    
    # Notification pour créer un compte (toutes les 10 articles lus)
    session_views = request.session.get('article_views', [])
    if len(session_views) % 10 == 0 and len(session_views) > 0:
        Notification.objects.create(
            session_key=session_key,
            type_notif='auth_required',
            titre='📝 Créer un compte',
            message='Créez un compte pour commenter, ajouter des articles et accéder aux forums!',
        )

