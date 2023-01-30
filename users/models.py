from django.db import models
from django.contrib.auth.models import User


class ProfileUser(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, null=False)
    is_admin = models.BooleanField(
        blank=False, null=False, default=False)

    def __str__(self):
        return self.user.first_name
