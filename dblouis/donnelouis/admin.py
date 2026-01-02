from django.contrib import admin
from .models import Article, ImageArticle

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