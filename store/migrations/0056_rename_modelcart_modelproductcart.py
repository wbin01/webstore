# Generated by Django 4.1.5 on 2023-02-03 12:46

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0055_rename_modelhighlightproducts_modelproducthighlight'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ModelCart',
            new_name='ModelProductCart',
        ),
    ]