# Generated by Django 4.1.5 on 2023-02-05 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0062_modelstoreprofile_theme_body_background_color'),
    ]

    operations = [
        migrations.RenameField(
            model_name='modelstoreprofile',
            old_name='theme_admin_background_color',
            new_name='theme_admin_color',
        ),
        migrations.RenameField(
            model_name='modelstoreprofile',
            old_name='theme_background_color',
            new_name='theme_color',
        ),
    ]
