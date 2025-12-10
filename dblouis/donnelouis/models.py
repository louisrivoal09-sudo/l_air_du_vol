from django.db import models

class Article(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    auteur = models.CharField(max_length=100)
    date_publication = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre
