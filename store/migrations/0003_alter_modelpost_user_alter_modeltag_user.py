# Generated by Django 4.1.5 on 2023-01-28 19:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profileuser_delete_modeluser'),
        ('store', '0002_rename_modeltags_modeltag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelpost',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profileuser'),
        ),
        migrations.AlterField(
            model_name='modeltag',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profileuser'),
        ),
    ]
