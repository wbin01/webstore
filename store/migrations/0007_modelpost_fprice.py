# Generated by Django 4.1.5 on 2023-01-28 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_modelpost_price_alter_modelpost_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='modelpost',
            name='fprice',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
