# Generated by Django 4.1.5 on 2023-02-02 15:09

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0047_modelbuy_publication_date_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ModelFavorites',
            new_name='ModelFavorite',
        ),
    ]
