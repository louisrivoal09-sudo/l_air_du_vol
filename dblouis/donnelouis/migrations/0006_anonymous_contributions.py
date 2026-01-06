# Generated migration for anonymous forum contributions

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('donnelouis', '0005_forumreponse_votes_forumvote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forumsujet',
            name='auteur',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sujets_forum', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='forumsujet',
            name='auteur_email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='forumsujet',
            name='auteur_nom',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='forumreponse',
            name='auteur',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='forumreponse',
            name='auteur_email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='forumreponse',
            name='auteur_nom',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
