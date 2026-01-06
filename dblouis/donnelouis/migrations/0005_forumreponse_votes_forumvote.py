# Generated migration for forum improvements

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('donnelouis', '0004_alter_lien_options_forumsujet_forumreponse'),
    ]

    operations = [
        migrations.AddField(
            model_name='forumreponse',
            name='votes',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='ForumVote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_vote', models.IntegerField(choices=[(1, 'Utile'), (-1, 'Non utile')])),
                ('date_vote', models.DateTimeField(auto_now_add=True)),
                ('reponse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vote_reponse', to='donnelouis.forumreponse')),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Vote forum',
                'verbose_name_plural': 'Votes forum',
            },
        ),
        migrations.AddConstraint(
            model_name='forumvote',
            constraint=models.UniqueConstraint(fields=('reponse', 'utilisateur'), name='unique_vote_per_user'),
        ),
    ]
