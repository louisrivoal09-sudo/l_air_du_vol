# Generated migration for Contact model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donnelouis', '0002_media_lien'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('sujet', models.CharField(max_length=200)),
                ('message', models.TextField()),
                ('date_envoi', models.DateTimeField(auto_now_add=True)),
                ('lu', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Message de contact',
                'verbose_name_plural': 'Messages de contact',
                'ordering': ['-date_envoi'],
            },
        ),
    ]
