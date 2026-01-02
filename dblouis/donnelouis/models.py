from django.db import models
from django.utils.text import slugify

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
