# Generated by Django 4.1.5 on 2023-02-05 18:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0066_rename_theme_admin_color_modelstoreprofile_theme_color_admin'),
    ]

    operations = [
        migrations.RenameField(
            model_name='modelstoreprofile',
            old_name='theme_background_color',
            new_name='background_color',
        ),
    ]
