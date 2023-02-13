# Generated by Django 4.1.5 on 2023-02-13 01:20

from django.db import migrations, models
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0075_remove_modelproduct_price_off'),
    ]

    operations = [
        migrations.AddField(
            model_name='modelproduct',
            name='price_off',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='modelproduct',
            name='image_1',
            field=django_resized.forms.ResizedImageField(crop=['middle', 'center'], force_format=None, keep_meta=True, quality=-1, scale=None, size=[500, 500], upload_to='img_posts/'),
        ),
        migrations.AlterField(
            model_name='modelproduct',
            name='image_2',
            field=django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format=None, keep_meta=True, null=True, quality=-1, scale=None, size=[500, 500], upload_to='img_posts/'),
        ),
        migrations.AlterField(
            model_name='modelproduct',
            name='image_3',
            field=django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format=None, keep_meta=True, null=True, quality=-1, scale=None, size=[500, 500], upload_to='img_posts/'),
        ),
        migrations.AlterField(
            model_name='modelproduct',
            name='image_4',
            field=django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format=None, keep_meta=True, null=True, quality=-1, scale=None, size=[500, 500], upload_to='img_posts/'),
        ),
        migrations.AlterField(
            model_name='modelproduct',
            name='image_5',
            field=django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format=None, keep_meta=True, null=True, quality=-1, scale=None, size=[500, 500], upload_to='img_posts/'),
        ),
    ]
