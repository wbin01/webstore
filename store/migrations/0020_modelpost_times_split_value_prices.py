# Generated by Django 4.1.5 on 2023-01-30 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_modelpost_shipping_price_modelpost_times_split_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='modelpost',
            name='times_split_value_prices',
            field=models.FloatField(default=0.0),
        ),
    ]
