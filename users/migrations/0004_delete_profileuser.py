# Generated by Django 4.1.5 on 2023-02-01 00:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_modeluser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProfileUser',
        ),
    ]
