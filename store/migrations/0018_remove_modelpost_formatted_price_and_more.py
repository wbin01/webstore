# Generated by Django 4.1.5 on 2023-01-30 00:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_alter_modelpost_content_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modelpost',
            name='formatted_price',
        ),
        migrations.RemoveField(
            model_name='modelpost',
            name='formatted_shipping_price',
        ),
        migrations.RemoveField(
            model_name='modelpost',
            name='formatted_times_split_price',
        ),
    ]
