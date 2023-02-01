from django.db import models
from django.contrib.auth.models import User


class ModelUser(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    username = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField(max_length=100, blank=False, null=False)
    password = models.CharField(max_length=30, blank=False, null=False)
    password_confirm = models.CharField(max_length=30, blank=False, null=False)

    def __str__(self):
        return self.name
