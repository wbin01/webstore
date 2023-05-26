# import datetime
# import string
# import logging

from django.shortcuts import get_object_or_404

import store.models as models


def get_user_profile(request) -> models.ModelUserProfile:
    """..."""
    try:
        return get_object_or_404(
            models.ModelUserProfile, user=request.user.id)
    except Exception as err:
        logging.error(err)
        profile = models.ModelUserProfile.objects.create(
            user=request.user,
            is_admin=False,
            is_superuser=False)
        profile.save()
        return get_object_or_404(
            models.ModelUserProfile, user=request.user.id)
