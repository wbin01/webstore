# Generated by Django 4.1.5 on 2023-02-03 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0058_remove_modelproductcart_product_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='modelproductcart',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]