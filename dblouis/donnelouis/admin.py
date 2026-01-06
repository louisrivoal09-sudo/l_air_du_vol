from django.contrib import admin
from .models import (
    Article, ImageArticle, Media, Lien, Contact, ForumSujet, ForumReponse,
    UserProfile, FavoriteArticle, ArticleComment, ArticleReport, Avion, OfflineCache,
    Notification, CommentNotification
)

class ImageArticleInline(admin.TabularInline):
    model = ImageArticle
    extra = 3
    fields = ('image_url', 'legende', 'ordre')

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('titre', 'categorie', 'auteur', 'date_publication')
    list_filter = ('categorie', 'date_publication')
    search_fields = ('titre', 'resume')
    prepopulated_fields = {'slug': ('titre',)}
    date_hierarchy = 'date_publication'
    inlines = [ImageArticleInline]
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('titre', 'slug', 'categorie', 'auteur', 'date_publication', 'image_principale')
        }),
        ('Résumé', {
            'fields': ('resume',)
        }),
        ('Thème 1', {
            'fields': ('theme1_titre', 'theme1_section_a_titre', 'theme1_section_a_texte', 
                      'theme1_section_b_titre', 'theme1_section_b_texte'),
            'classes': ('collapse',)
        }),
        ('Thème 2', {
            'fields': ('theme2_titre', 'theme2_section_a_titre', 'theme2_section_a_texte',
                      'theme2_section_b_titre', 'theme2_section_b_texte'),
            'classes': ('collapse',)
        }),
        ('Thème 3', {
            'fields': ('theme3_titre', 'theme3_section_a_titre', 'theme3_section_a_texte',
                      'theme3_section_b_titre', 'theme3_section_b_texte'),
            'classes': ('collapse',)
        }),
        ('Conclusion', {
            'fields': ('conclusion_titre', 'conclusion_texte')
        }),
    )

@admin.register(ImageArticle)
class ImageArticleAdmin(admin.ModelAdmin):
    list_display = ('article', 'ordre', 'legende')
    list_filter = ('article',)


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('titre', 'type_media', 'auteur', 'date_publication')
    list_filter = ('type_media', 'date_publication')
    search_fields = ('titre', 'description')
    prepopulated_fields = {'slug': ('titre',)}
    date_hierarchy = 'date_publication'
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('titre', 'slug', 'type_media', 'auteur', 'date_publication')
        }),
        ('Contenu', {
            'fields': ('description', 'url_media', 'image_principale')
        }),
    )


@admin.register(Lien)
class LienAdmin(admin.ModelAdmin):
    list_display = ('titre', 'categorie', 'url')
    list_filter = ('categorie',)
    search_fields = ('titre', 'description', 'url')
    prepopulated_fields = {'slug': ('titre',)}
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('titre', 'slug', 'categorie')
        }),
        ('Contenu', {
            'fields': ('description', 'url', 'image_principale')
        }),
    )


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'sujet')
    search_fields = ('nom', 'email', 'sujet', 'message')
    readonly_fields = ('nom', 'email', 'sujet', 'message')
    fieldsets = (
        ('Message', {
            'fields': ('nom', 'email', 'sujet', 'message')
        }),
    )


class ForumReponseInline(admin.TabularInline):
    model = ForumReponse
    extra = 0
    fields = ('auteur', 'contenu', 'date_creation')
    readonly_fields = ('auteur', 'date_creation')


@admin.register(ForumSujet)
class ForumSujetAdmin(admin.ModelAdmin):
    list_display = ('titre', 'categorie', 'auteur', 'date_creation', 'vues')
    list_filter = ('categorie', 'date_creation')
    search_fields = ('titre', 'contenu', 'tags')
    prepopulated_fields = {'slug': ('titre',)}
    date_hierarchy = 'date_creation'
    inlines = [ForumReponseInline]
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('titre', 'slug', 'categorie', 'auteur')
        }),
        ('Contenu', {
            'fields': ('contenu', 'tags')
        }),
        ('Statistiques', {
            'fields': ('vues', 'date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('date_creation', 'date_modification')


@admin.register(ForumReponse)
class ForumReponseAdmin(admin.ModelAdmin):
    list_display = ('sujet', 'auteur', 'date_creation')
    list_filter = ('sujet', 'date_creation')
    search_fields = ('sujet__titre', 'contenu', 'auteur__username')
    readonly_fields = ('date_creation', 'date_modification')
    date_hierarchy = 'date_creation'
    
    fieldsets = (
        ('Sujet', {
            'fields': ('sujet',)
        }),
        ('Contenu', {
            'fields': ('auteur', 'contenu')
        }),
        ('Métadonnées', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )


# ============================================================================
# NOUVEAUX MODÈLES ADMIN
# ============================================================================

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nombre_articles_lus', 'nombre_posts_forum', 'date_inscription')
    list_filter = ('date_inscription',)
    search_fields = ('user__username', 'bio')
    readonly_fields = ('date_inscription', 'date_modification')
    
    fieldsets = (
        ('Utilisateur', {
            'fields': ('user',)
        }),
        ('Profil', {
            'fields': ('bio', 'avatar_url')
        }),
        ('Statistiques', {
            'fields': ('nombre_articles_lus', 'nombre_posts_forum', 'nombre_commentaires')
        }),
        ('Métadonnées', {
            'fields': ('date_inscription', 'date_modification'),
            'classes': ('collapse',)
        }),
    )


@admin.register(FavoriteArticle)
class FavoriteArticleAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'date_ajout')
    list_filter = ('date_ajout', 'user')
    search_fields = ('user__username', 'article__titre')
    date_hierarchy = 'date_ajout'
    
    fieldsets = (
        ('Favori', {
            'fields': ('user', 'article')
        }),
        ('Métadonnées', {
            'fields': ('date_ajout',),
            'classes': ('collapse',)
        }),
    )


@admin.register(ArticleComment)
class ArticleCommentAdmin(admin.ModelAdmin):
    list_display = ('get_auteur_display', 'article', 'date_creation', 'approuve')
    list_filter = ('approuve', 'date_creation', 'article')
    search_fields = ('auteur__username', 'auteur_nom', 'article__titre', 'contenu')
    date_hierarchy = 'date_creation'
    
    fieldsets = (
        ('Article', {
            'fields': ('article',)
        }),
        ('Auteur', {
            'fields': ('auteur', 'auteur_nom', 'auteur_email')
        }),
        ('Contenu', {
            'fields': ('contenu',)
        }),
        ('Modération', {
            'fields': ('approuve',)
        }),
        ('Métadonnées', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('date_creation', 'date_modification')


@admin.register(ArticleReport)
class ArticleReportAdmin(admin.ModelAdmin):
    list_display = ('article', 'raison', 'date_signalement', 'traite')
    list_filter = ('raison', 'date_signalement', 'traite')
    search_fields = ('article__titre', 'description')
    date_hierarchy = 'date_signalement'
    
    fieldsets = (
        ('Article', {
            'fields': ('article',)
        }),
        ('Signalement', {
            'fields': ('signaleur', 'raison', 'description')
        }),
        ('Traitement', {
            'fields': ('traite',)
        }),
        ('Métadonnées', {
            'fields': ('date_signalement',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('date_signalement',)


@admin.register(Avion)
class AvionAdmin(admin.ModelAdmin):
    list_display = ('nom', 'constructeur', 'type_avion', 'annee_premier_vol', 'capacite')
    list_filter = ('type_avion', 'constructeur')
    search_fields = ('nom', 'constructeur', 'type_avion')
    prepopulated_fields = {'slug': ('nom',)}
    fieldsets = (
        ('Informations de base', {
            'fields': ('nom', 'slug', 'constructeur', 'type_avion', 'annee_premier_vol', 'capacite', 'image_principale')
        }),
        ('Description', {
            'fields': ('description',)
        }),
    )
    readonly_fields = ('date_creation', 'date_modification')


@admin.register(OfflineCache)
class OfflineCacheAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_cache', 'date_derniere_sync')
    list_filter = ('date_cache', 'date_derniere_sync', 'user')
    search_fields = ('user__username',)
    readonly_fields = ('date_cache', 'date_derniere_sync')
    date_hierarchy = 'date_cache'
    
    fieldsets = (
        ('Utilisateur', {
            'fields': ('user',)
        }),
        ('Contenu en Cache', {
            'fields': ('article', 'avion', 'media')
        }),
        ('Métadonnées', {
            'fields': ('date_cache', 'date_derniere_sync'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('type_notif', 'titre', 'utilisateur', 'lue', 'date_creation')
    list_filter = ('type_notif', 'lue', 'date_creation')
    search_fields = ('titre', 'message', 'utilisateur__username')
    readonly_fields = ('date_creation',)
    date_hierarchy = 'date_creation'
    
    fieldsets = (
        ('Notification', {
            'fields': ('type_notif', 'titre', 'message')
        }),
        ('Destinataire', {
            'fields': ('utilisateur', 'session_key')
        }),
        ('Liens', {
            'fields': ('article', 'media', 'sujet_forum'),
            'classes': ('collapse',)
        }),
        ('Statut', {
            'fields': ('lue', 'date_creation'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CommentNotification)
class CommentNotificationAdmin(admin.ModelAdmin):
    list_display = ('comment', 'auteur_du_commentaire_original', 'lue', 'date_creation')
    list_filter = ('lue', 'date_creation')
    search_fields = ('comment__contenu', 'auteur_du_commentaire_original__username')
    readonly_fields = ('date_creation',)
    date_hierarchy = 'date_creation'