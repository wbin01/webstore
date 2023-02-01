# Generated by Django 4.1.5 on 2023-02-01 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_delete_profileuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modeluser',
            name='email',
            field=models.EmailField(max_length=100),
        ),
        migrations.AlterField(
            model_name='modeluser',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='modeluser',
            name='password',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='modeluser',
            name='password_confirm',
            field=models.CharField(max_length=30),
        ),
    ]
