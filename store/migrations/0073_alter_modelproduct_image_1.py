# Generated by Django 4.1.5 on 2023-02-13 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0072_rename_modelproductcart_modelcart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelproduct',
            name='image_1',
            field=models.ImageField(upload_to='img_posts/%d/%m/%Y/'),
        ),
    ]
