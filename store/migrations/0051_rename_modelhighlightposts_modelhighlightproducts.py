# Generated by Django 4.1.5 on 2023-02-03 00:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0050_modelproduct_available_quantity_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ModelHighlightPosts',
            new_name='ModelHighlightProducts',
        ),
    ]