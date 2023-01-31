# Generated by Django 4.1.5 on 2023-01-31 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0028_alter_modelpost_content_alter_modelpost_summary_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='modelstoreprofile',
            name='social_media_discord',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='modelstoreprofile',
            name='social_media_facebook',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='modelstoreprofile',
            name='social_media_github',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='modelstoreprofile',
            name='social_media_instagram',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='modelstoreprofile',
            name='social_media_linkedin',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='modelstoreprofile',
            name='social_media_other',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='modelstoreprofile',
            name='social_media_twitch',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='modelstoreprofile',
            name='social_media_twitter',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='modelstoreprofile',
            name='social_media_whatsapp',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='modelstoreprofile',
            name='social_media_youtube',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
