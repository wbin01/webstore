# Generated by Django 4.1.5 on 2023-02-02 12:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0046_rename_modelpost_modelproduct'),
    ]

    operations = [
        migrations.AddField(
            model_name='modelbuy',
            name='publication_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='modelfavorites',
            name='publication_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
