from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

# ImageField -> pip install Pillow

# https://github.com/un1t/django-resized
from django_resized import ResizedImageField  # pip: Pillow, django-resized

# https://github.com/fabiocaccamo/django-colorfield
from colorfield.fields import ColorField  # pip: django-colorfield


class ModelPost(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, null=False)
    title = models.CharField(
        max_length=200, blank=False, null=False, default='Título')
    old_price = models.FloatField(
        blank=False, null=False, default=0.0)
    new_price = models.FloatField(
        blank=False, null=False, default=0.0)
    show_off_price = models.BooleanField(
        default=True, blank=False, null=False)
    times_split_num = models.IntegerField(
        blank=False, null=False, default=0)
    times_split_interest = models.IntegerField(
        blank=False, null=False, default=0)
    shipping_price = models.FloatField(
        blank=False, null=False, default=0.0)
    image_1 = ResizedImageField(
        size=[500, 500], crop=['middle', 'center'],
        upload_to='img_posts/%d/%m/%Y/', blank=False, null=False)
    image_2 = ResizedImageField(
        size=[500, 500], crop=['middle', 'center'],
        upload_to='img_posts/%d/%m/%Y/', blank=True, null=True)
    image_3 = ResizedImageField(
        size=[500, 500], crop=['middle', 'center'],
        upload_to='img_posts/%d/%m/%Y/', blank=True, null=True)
    image_4 = ResizedImageField(
        size=[500, 500], crop=['middle', 'center'],
        upload_to='img_posts/%d/%m/%Y/', blank=True, null=True)
    image_5 = ResizedImageField(
        size=[500, 500], crop=['middle', 'center'],
        upload_to='img_posts/%d/%m/%Y/', blank=True, null=True)
    summary = models.CharField(
        max_length=100, default='...', blank=True, null=True)
    content = models.TextField(
        default='...', blank=True, null=True)
    tags = models.CharField(
        max_length=100, blank=False, null=False, default='Tag 1, Tag 2')
    publication_date = models.DateTimeField(
        default=datetime.now, blank=True)
    is_published = models.BooleanField(
        default=False, blank=False, null=False)

    def __str__(self):
        return self.title


class ModelHighlightPosts(models.Model):
    post = models.ForeignKey(
        ModelPost, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return self.post.title


class ModelStoreProfile(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, null=False)
    brand_name = models.CharField(
        max_length=200, blank=False, null=False)
    show_brand_name_on_nav = models.BooleanField(
        default=False, blank=False, null=False)
    brand_image = ResizedImageField(
        size=[80, 40], crop=['middle', 'center'],
        upload_to='img_store/', blank=True, null=True)
    show_brand_image_on_nav = models.BooleanField(
        default=True, blank=False, null=False)
    theme_text_color = ColorField(
        blank=True, null=True, default='#FFFFFF')
    theme_background_color = ColorField(
        blank=True, null=True, default='#8A42AA')
    social_media_facebook = models.CharField(
        max_length=200, blank=True, null=True)
    social_media_whatsapp = models.CharField(
        max_length=200, blank=True, null=True)
    social_media_twitter = models.CharField(
        max_length=200, blank=True, null=True)
    social_media_youtube = models.CharField(
        max_length=200, blank=True, null=True)
    social_media_instagram = models.CharField(
        max_length=200, blank=True, null=True)
    social_media_twitch = models.CharField(
        max_length=200, blank=True, null=True)
    social_media_discord = models.CharField(
        max_length=200, blank=True, null=True)
    social_media_linkedin = models.CharField(
        max_length=200, blank=True, null=True)
    social_media_github = models.CharField(
        max_length=200, blank=True, null=True)
    social_media_other = models.CharField(
        max_length=200, blank=True, null=True)

    def __str__(self):
        return self.brand_name


class ModelUserProfile(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, null=False)
    profile_image = ResizedImageField(
        size=[40, 40], crop=['middle', 'center'],
        upload_to='img_profile/', blank=True, null=True)
    is_admin = models.BooleanField(
        blank=False, null=False, default=False)
    is_superuser = models.BooleanField(
        blank=False, null=False, default=False)

    def __str__(self):
        return self.user.first_name
