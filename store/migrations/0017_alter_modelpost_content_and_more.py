# Generated by Django 4.1.5 on 2023-01-29 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_remove_modelpost_tag_1_modelpost_tags_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelpost',
            name='content',
            field=models.TextField(blank=True, default='Exemplo...', null=True),
        ),
        migrations.AlterField(
            model_name='modelpost',
            name='formatted_price',
            field=models.CharField(blank=True, default='R$ 0,00', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='modelpost',
            name='formatted_shipping_price',
            field=models.CharField(blank=True, default='Frete grátis', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='modelpost',
            name='formatted_times_split_price',
            field=models.CharField(blank=True, default='1x R$ 0,00', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='modelpost',
            name='summary',
            field=models.TextField(blank=True, default='Exemplo...', null=True),
        ),
        migrations.AlterField(
            model_name='modelpost',
            name='title',
            field=models.CharField(default='Título', max_length=200),
        ),
    ]
