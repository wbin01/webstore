# Generated by Django 4.1.5 on 2023-02-01 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0040_rename_profileuser_modelprofileuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='modelprofileuser',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]
