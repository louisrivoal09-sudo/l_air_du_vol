# Generated migration for Media and Lien models

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('donnelouis', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, max_length=220, unique=True)),
                ('type_media', models.CharField(choices=[('video', 'Vidéo'), ('podcast', 'Podcast')], default='video', max_length=50)),
                ('date_publication', models.DateField()),
                ('auteur', models.CharField(default="L'Air du Vol", max_length=100)),
                ('description', models.TextField(help_text='Description du média')),
                ('url_media', models.URLField(help_text='URL de la vidéo (YouTube, etc.) ou du podcast')),
                ('image_principale', models.URLField(blank=True, help_text='URL de l\'image miniature')),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('date_modification', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Média',
                'verbose_name_plural': 'Médias',
                'ordering': ['-date_publication'],
            },
        ),
        migrations.CreateModel(
            name='Lien',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, max_length=220, unique=True)),
                ('categorie', models.CharField(choices=[('aviation', 'Aviation'), ('ressources', 'Ressources'), ('communaute', 'Communauté'), ('outils', 'Outils')], default='ressources', max_length=50)),
                ('description', models.TextField(help_text='Description du lien')),
                ('url', models.URLField(help_text='URL cible du lien')),
                ('image_principale', models.URLField(blank=True, help_text='URL de l\'image du lien')),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('date_modification', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Lien',
                'verbose_name_plural': 'Liens',
                'ordering': ['categorie', 'titre'],
            },
        ),
    ]
