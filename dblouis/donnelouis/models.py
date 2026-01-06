from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Article(models.Model):
    CATEGORIES = [
        ('aviation', 'Aviation civile'),
        ('avions', 'Grands avions'),
        ('operations', 'Opérations militaires'),
    ]
    
    # Informations de base
    titre = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    categorie = models.CharField(max_length=50, choices=CATEGORIES, default='aviation')
    date_publication = models.DateField()
    auteur = models.CharField(max_length=100, default='L\'Air du Vol')
    
    # Résumé
    resume = models.TextField(help_text="Résumé de l'article")
    
    # Image principale
    image_principale = models.URLField(blank=True, help_text="URL de l'image principale")
    
    # Thème 1
    theme1_titre = models.CharField(max_length=200, blank=True)
    theme1_section_a_titre = models.CharField(max_length=200, blank=True)
    theme1_section_a_texte = models.TextField(blank=True)
    theme1_section_b_titre = models.CharField(max_length=200, blank=True)
    theme1_section_b_texte = models.TextField(blank=True)
    
    # Thème 2
    theme2_titre = models.CharField(max_length=200, blank=True)
    theme2_section_a_titre = models.CharField(max_length=200, blank=True)
    theme2_section_a_texte = models.TextField(blank=True)
    theme2_section_b_titre = models.CharField(max_length=200, blank=True)
    theme2_section_b_texte = models.TextField(blank=True)
    
    # Thème 3
    theme3_titre = models.CharField(max_length=200, blank=True)
    theme3_section_a_titre = models.CharField(max_length=200, blank=True)
    theme3_section_a_texte = models.TextField(blank=True)
    theme3_section_b_titre = models.CharField(max_length=200, blank=True)
    theme3_section_b_texte = models.TextField(blank=True)
    
    # Conclusion
    conclusion_titre = models.CharField(max_length=200, default='Conclusion')
    conclusion_texte = models.TextField(blank=True)
    
    # Métadonnées
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_publication']
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.titre


class ImageArticle(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField()
    legende = models.CharField(max_length=300, blank=True)
    ordre = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['ordre']
    
    def __str__(self):
        return f"Image {self.ordre} - {self.article.titre}"


class Media(models.Model):
    TYPE_CHOICES = [
        ('video', 'Vidéo'),
        ('podcast', 'Podcast'),
    ]
    
    # Informations de base
    titre = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    type_media = models.CharField(max_length=50, choices=TYPE_CHOICES, default='video')
    date_publication = models.DateField()
    auteur = models.CharField(max_length=100, default='L\'Air du Vol')
    
    # Description
    description = models.TextField(help_text="Description du média")
    
    # URL du média
    url_media = models.URLField(help_text="URL de la vidéo (YouTube, etc.) ou du podcast")
    
    # Thumbnail/Image
    image_principale = models.URLField(blank=True, help_text="URL de l'image miniature")
    
    # Métadonnées
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_publication']
        verbose_name = 'Média'
        verbose_name_plural = 'Médias'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.titre


class Lien(models.Model):
    CATEGORIES = [
        ('aviation', 'Aviation'),
        ('ressources', 'Ressources'),
        ('communaute', 'Communauté'),
        ('outils', 'Outils'),
    ]
    
    # Informations de base
    titre = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    categorie = models.CharField(max_length=50, choices=CATEGORIES, default='ressources')
    
    # Descriptif
    description = models.TextField(help_text="Description du lien")
    
    # URL du lien
    url = models.URLField(help_text="URL cible du lien")
    
    # Image
    image_principale = models.URLField(blank=True, help_text="URL de l'image du lien")
    
    # Métadonnées
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.titre


class Contact(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    sujet = models.CharField(max_length=200)
    message = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-date_envoi']
        verbose_name = 'Message de contact'
        verbose_name_plural = 'Messages de contact'
    
    def __str__(self):
        return f"{self.nom} - {self.sujet}"


# ===== MODÈLE POUR LE CATALOGUE D'AVION =====

class Avion(models.Model):
    nom = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    constructeur = models.CharField(max_length=200, blank=True)
    type_avion = models.CharField(max_length=100, blank=True)
    annee_premier_vol = models.IntegerField(blank=True, null=True)
    capacite = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True)
    image_principale = models.URLField(blank=True, help_text="URL de l'image principale")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom
    
    class Meta:
        ordering = ['-date_creation']
        verbose_name = 'Avion'
        verbose_name_plural = 'Avions'


# ===== MODÈLES FORUM =====

class ForumSujet(models.Model):
    CATEGORIES = [
        ('general', 'Général'),
        ('technique', 'Technique'),
        ('aviation', 'Aviation'),
        ('actualites', 'Actualités'),
    ]
    
    # Informations de base
    titre = models.CharField(max_length=300)
    slug = models.SlugField(max_length=320, unique=True, blank=True)
    categorie = models.CharField(max_length=50, choices=CATEGORIES, default='general')
    
    # Auteur et contenu
    auteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sujets_forum', null=True, blank=True)
    auteur_nom = models.CharField(max_length=100, blank=True, help_text="Nom si non connecté")
    auteur_email = models.EmailField(blank=True, help_text="Email si non connecté")
    contenu = models.TextField()
    
    # Tags et métadonnées
    tags = models.CharField(max_length=200, blank=True, help_text="Tags séparés par des virgules")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    # Statistiques
    vues = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-date_creation']
        verbose_name = 'Sujet de forum'
        verbose_name_plural = 'Sujets de forum'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.titre
    
    def get_nombre_reponses(self):
        return self.reponses.count()
    
    def get_auteur_display(self):
        """Retourne le nom de l'auteur (connecté ou anonyme)"""
        if self.auteur:
            return self.auteur.username
        return self.auteur_nom or "Anonyme"


class ForumReponse(models.Model):
    # Relations
    sujet = models.ForeignKey(ForumSujet, on_delete=models.CASCADE, related_name='reponses')
    auteur = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    auteur_nom = models.CharField(max_length=100, blank=True, help_text="Nom si non connecté")
    auteur_email = models.EmailField(blank=True, help_text="Email si non connecté")
    
    # Contenu
    contenu = models.TextField()
    
    # Métadonnées
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    # Statistiques
    votes = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['date_creation']
        verbose_name = 'Réponse de forum'
        verbose_name_plural = 'Réponses de forum'
    
    def __str__(self):
        auteur_name = self.auteur.username if self.auteur else (self.auteur_nom or "Anonyme")
        return f"Réponse de {auteur_name} à {self.sujet.titre}"
    
    def get_auteur_display(self):
        """Retourne le nom de l'auteur (connecté ou anonyme)"""
        if self.auteur:
            return self.auteur.username
        return self.auteur_nom or "Anonyme"
    
    def get_votes_count(self):
        return self.votes


class ForumVote(models.Model):
    """Modèle pour tracker les votes (likes) sur les réponses du forum"""
    VOTE_CHOICES = [
        (1, 'Utile'),
        (-1, 'Non utile'),
    ]
    
    reponse = models.ForeignKey(ForumReponse, on_delete=models.CASCADE, related_name='vote_reponse')
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    type_vote = models.IntegerField(choices=VOTE_CHOICES)
    date_vote = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('reponse', 'utilisateur')
        verbose_name = 'Vote forum'
        verbose_name_plural = 'Votes forum'
    
    def __str__(self):
        return f"Vote de {self.utilisateur.username} sur réponse #{self.reponse.id}"


# ============================================================================
# NOUVEAUX MODÈLES
# ============================================================================

class UserProfile(models.Model):
    """Profil utilisateur enrichi"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, max_length=500, help_text="Courte bio personnelle")
    avatar_url = models.URLField(blank=True, help_text="URL de l'avatar")
    date_inscription = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    # Statistiques
    nombre_articles_lus = models.IntegerField(default=0)
    nombre_posts_forum = models.IntegerField(default=0)
    nombre_commentaires = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'Profil utilisateur'
        verbose_name_plural = 'Profils utilisateur'
    
    def __str__(self):
        return f"Profil de {self.user.username}"


class FavoriteArticle(models.Model):
    """Articles favoris des utilisateurs"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles_favoris')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='favoris')
    date_ajout = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'article')
        ordering = ['-date_ajout']
        verbose_name = 'Article favori'
        verbose_name_plural = 'Articles favoris'
    
    def __str__(self):
        return f"{self.user.username} - {self.article.titre}"


class ArticleComment(models.Model):
    """Commentaires sur les articles"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='commentaires')
    auteur = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    auteur_nom = models.CharField(max_length=100, blank=True, help_text="Nom si non connecté")
    auteur_email = models.EmailField(blank=True, help_text="Email si non connecté")
    
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    approuve = models.BooleanField(default=True, help_text="À modérer si false")
    
    class Meta:
        ordering = ['date_creation']
        verbose_name = 'Commentaire article'
        verbose_name_plural = 'Commentaires article'
    
    def __str__(self):
        auteur = self.auteur.username if self.auteur else (self.auteur_nom or "Anonyme")
        return f"Commentaire de {auteur} sur {self.article.titre}"
    
    def get_auteur_display(self):
        if self.auteur:
            return self.auteur.username
        return self.auteur_nom or "Anonyme"


class ArticleReport(models.Model):
    """Signalements d'articles inappropriés"""
    RAISONS = [
        ('spam', 'Spam'),
        ('offensant', 'Contenu offensant'),
        ('inexact', 'Information inexacte'),
        ('publicite', 'Publicité non autorisée'),
        ('autre', 'Autre'),
    ]
    
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='signalements')
    signaleur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    raison = models.CharField(max_length=50, choices=RAISONS)
    description = models.TextField(blank=True, help_text="Détails du signalement")
    date_signalement = models.DateTimeField(auto_now_add=True)
    traite = models.BooleanField(default=False, help_text="Signalement traité par modérateur")
    
    class Meta:
        ordering = ['-date_signalement']
        verbose_name = 'Signalement article'
        verbose_name_plural = 'Signalements article'
    
    def __str__(self):
        signaleur = self.signaleur.username if self.signaleur else "Anonyme"
        return f"Signalement de {signaleur} sur {self.article.titre}"




class OfflineCache(models.Model):
    """Cache pour mode offline - articles et médias favoris"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offline_cache')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True)
    media = models.ForeignKey(Media, on_delete=models.CASCADE, null=True, blank=True)
    
    date_cache = models.DateTimeField(auto_now_add=True)
    date_derniere_sync = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_cache']
        verbose_name = 'Cache offline'
        verbose_name_plural = 'Caches offline'
    
    def __str__(self):
        if self.article:
            return f"Cache: {self.article.titre}"
        elif self.media:
            return f"Cache: {self.media.titre}"
        return "Cache vide"


# ============================================================================
# MODÈLES DE NOTIFICATIONS EN TEMPS RÉEL
# ============================================================================

class Notification(models.Model):
    """Notifications en temps réel pour les utilisateurs"""
    TYPE_CHOICES = [
        ('forum_reponse', 'Réponse au forum'),
        ('forum_mention', 'Mention au forum'),
        ('article_nouveau', 'Nouvel article'),
        ('media_nouveau', 'Nouveau média'),
        ('catalogue_nouveau', 'Nouvel avion'),
        ('commentaire_reponse', 'Réponse à votre commentaire'),
        ('auth_required', 'Créer un compte'),
    ]
    
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    session_key = models.CharField(max_length=40, blank=True, help_text="Pour utilisateurs non connectés")
    
    type_notif = models.CharField(max_length=50, choices=TYPE_CHOICES)
    titre = models.CharField(max_length=200)
    message = models.TextField()
    
    # Liens optionnels vers les objets
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True)
    media = models.ForeignKey(Media, on_delete=models.CASCADE, null=True, blank=True)
    sujet_forum = models.ForeignKey(ForumSujet, on_delete=models.CASCADE, null=True, blank=True)
    
    lue = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_creation']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
    
    def __str__(self):
        return f"{self.type_notif} - {self.titre}"
    
    def marquer_comme_lue(self):
        self.lue = True
        self.save()


class CommentNotification(models.Model):
    """Notifications spécifiques pour les commentaires"""
    comment = models.ForeignKey(ArticleComment, on_delete=models.CASCADE, related_name='notifications')
    auteur_du_commentaire_original = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    date_creation = models.DateTimeField(auto_now_add=True)
    lue = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Notification commentaire'
        verbose_name_plural = 'Notifications commentaires'
    
    def __str__(self):
        return f"Notif: Réponse à commentaire"


# ============================================================================
# SYSTÈME DE LIKE/DISLIKE
# ============================================================================

class ArticleLike(models.Model):
    """Likes/Dislikes sur les articles"""
    VOTE_CHOICES = [
        (1, 'J\'aime'),
        (-1, 'J\'aime pas'),
    ]
    
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='likes')
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    type_vote = models.IntegerField(choices=VOTE_CHOICES, default=1)
    date_vote = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('article', 'utilisateur')
        verbose_name = 'Like article'
        verbose_name_plural = 'Likes articles'
    
    def __str__(self):
        return f"{self.utilisateur.username} - {self.article.titre} ({self.get_type_vote_display()})"


class ForumSujetLike(models.Model):
    """Likes/Dislikes sur les sujets du forum"""
    VOTE_CHOICES = [
        (1, 'J\'aime'),
        (-1, 'J\'aime pas'),
    ]
    
    sujet = models.ForeignKey(ForumSujet, on_delete=models.CASCADE, related_name='likes')
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    type_vote = models.IntegerField(choices=VOTE_CHOICES, default=1)
    date_vote = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('sujet', 'utilisateur')
        verbose_name = 'Like sujet forum'
        verbose_name_plural = 'Likes sujets forum'
    
    def __str__(self):
        return f"{self.utilisateur.username} - {self.sujet.titre} ({self.get_type_vote_display()})"


class ForumReponseLike(models.Model):
    """Likes/Dislikes sur les réponses du forum"""
    VOTE_CHOICES = [
        (1, 'J\'aime'),
        (-1, 'J\'aime pas'),
    ]
    
    reponse = models.ForeignKey(ForumReponse, on_delete=models.CASCADE, related_name='likes')
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    type_vote = models.IntegerField(choices=VOTE_CHOICES, default=1)
    date_vote = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('reponse', 'utilisateur')
        verbose_name = 'Like réponse forum'
        verbose_name_plural = 'Likes réponses forum'
    
    def __str__(self):
        return f"{self.utilisateur.username} - Réponse #{self.reponse.id} ({self.get_type_vote_display()})"


class MediaLike(models.Model):
    """Likes/Dislikes sur les médias"""
    VOTE_CHOICES = [
        (1, 'J\'aime'),
        (-1, 'J\'aime pas'),
    ]
    
    media = models.ForeignKey(Media, on_delete=models.CASCADE, related_name='likes')
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    type_vote = models.IntegerField(choices=VOTE_CHOICES, default=1)
    date_vote = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('media', 'utilisateur')
        verbose_name = 'Like média'
        verbose_name_plural = 'Likes médias'
    
    def __str__(self):
        return f"{self.utilisateur.username} - {self.media.titre} ({self.get_type_vote_display()})"
