# ============================================================================
# SIGNAUX DJANGO - Notifications en temps réel
# ============================================================================
# Déclenche automatiquement des notifications lors de:
# - Création d'un nouvel article
# - Création d'une nouvelle discussion forum
# - Ajout d'une réponse forum
# - Ajout d'un commentaire article

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Article, ForumSujet, ForumReponse, ArticleComment, Media, Notification


@receiver(post_save, sender=Article)
def notify_new_article(sender, instance, created, **kwargs):
    """Notifie tous les utilisateurs d'un nouvel article"""
    if created:
        # Récupérer tous les utilisateurs actifs
        users = User.objects.filter(is_active=True).exclude(id=instance.auteur if hasattr(instance, 'auteur') and instance.auteur else None)
        
        for user in users:
            Notification.objects.create(
                utilisateur=user,
                type_notif='article_nouveau',
                titre=f"📰 Nouvel article: {instance.titre}",
                message=f"Découvrez le nouvel article '{instance.titre}' dans la catégorie {instance.categorie}",
                article=instance
            )


@receiver(post_save, sender=Media)
def notify_new_media(sender, instance, created, **kwargs):
    """Notifie tous les utilisateurs d'un nouveau média"""
    if created:
        users = User.objects.filter(is_active=True).exclude(id=instance.auteur if hasattr(instance, 'auteur') and instance.auteur else None)
        
        for user in users:
            Notification.objects.create(
                utilisateur=user,
                type_notif='media_nouveau',
                titre=f"🎥 Nouveau média: {instance.titre}",
                message=f"Un nouveau {instance.type_media} vient d'être publié: {instance.titre}",
                media=instance
            )


@receiver(post_save, sender=ForumSujet)
def notify_new_forum_subject(sender, instance, created, **kwargs):
    """Notifie les utilisateurs d'une nouvelle discussion forum"""
    if created:
        # Notifier tous les utilisateurs sauf l'auteur
        users = User.objects.filter(is_active=True).exclude(id=instance.auteur if instance.auteur else None)
        
        for user in users:
            Notification.objects.create(
                utilisateur=user,
                type_notif='forum_reponse',
                titre=f"💬 Nouvelle discussion: {instance.titre}",
                message=f"Une nouvelle discussion a été créée dans le forum: {instance.titre}",
                sujet_forum=instance
            )


@receiver(post_save, sender=ForumReponse)
def notify_new_forum_reply(sender, instance, created, **kwargs):
    """Notifie l'auteur du sujet qu'une réponse a été ajoutée"""
    if created:
        sujet = instance.sujet
        
        # Notifier l'auteur du sujet
        if sujet.auteur and sujet.auteur != instance.auteur:
            Notification.objects.create(
                utilisateur=sujet.auteur,
                type_notif='forum_reponse',
                titre=f"💬 Nouvelle réponse à: {sujet.titre}",
                message=f"{instance.get_auteur_display()} a répondu à votre discussion",
                sujet_forum=sujet
            )
        
        # Notifier les autres utilisateurs qui ont répondu au même sujet
        autres_auteurs = ForumReponse.objects.filter(
            sujet=sujet
        ).values_list('auteur_id', flat=True).distinct()
        
        for auteur_id in autres_auteurs:
            if auteur_id and auteur_id != instance.auteur_id and auteur_id != sujet.auteur_id:
                try:
                    auteur = User.objects.get(id=auteur_id)
                    Notification.objects.create(
                        utilisateur=auteur,
                        type_notif='forum_reponse',
                        titre=f"💬 Nouvelle réponse: {sujet.titre}",
                        message=f"Une nouvelle réponse a été ajoutée à une discussion que vous suivez",
                        sujet_forum=sujet
                    )
                except User.DoesNotExist:
                    pass


@receiver(post_save, sender=ArticleComment)
def notify_article_comment(sender, instance, created, **kwargs):
    """Notifie l'auteur quand un commentaire est ajouté à son article"""
    if created and instance.approuve:
        article = instance.article
        
        # Récupérer le créateur de l'article (si c'est un ForeignKey)
        # Sinon, on envoie une notification générale
        auteurs_article = User.objects.filter(is_active=True)
        
        for user in auteurs_article:
            # Éviter de notifier l'auteur du commentaire
            if instance.auteur and instance.auteur == user:
                continue
            
            Notification.objects.create(
                utilisateur=user,
                type_notif='commentaire_reponse',
                titre=f"💭 Nouveau commentaire sur: {article.titre}",
                message=f"{instance.get_auteur_display()} a commenté l'article '{article.titre}'",
                article=article
            )


# ============================================================================
# Configuration - À ajouter dans apps.py
# ============================================================================
# Dans donnelouis/apps.py, ajouter à la classe DonnelouisConfig:
#
# def ready(self):
#     import donnelouis.signals
