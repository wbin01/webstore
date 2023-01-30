# Generated by Django 4.1.5 on 2023-01-30 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_remove_modelpost_formatted_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='modelpost',
            name='shipping_price',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='modelpost',
            name='times_split_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='modelpost',
            name='times_split_price_interest',
            field=models.IntegerField(default=0),
        ),
    ]
