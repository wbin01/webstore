# Generated by Django 4.1.5 on 2023-01-30 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0022_modelpost_show_off_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='modelpost',
            old_name='price',
            new_name='old_price',
        ),
    ]
