# Generated by Django 4.1.5 on 2023-02-01 02:03

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0042_modelprofileuser_profile_image'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ModelProfileUser',
            new_name='ModelUserProfile',
        ),
    ]
