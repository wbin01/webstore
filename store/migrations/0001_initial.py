# Generated by Django 4.1.5 on 2023-01-28 16:53

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelTags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('image', models.ImageField(blank=True, upload_to='fotos/%d/%m/%Y/')),
                ('publication_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ModelPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('image', django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format=None, keep_meta=True, null=True, quality=-1, scale=None, size=[500, 300], upload_to='images/%d/%m/%Y/')),
                ('summary', models.TextField()),
                ('content', models.TextField()),
                ('publication_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('post_is_published', models.BooleanField(default=False)),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.modeltags')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
