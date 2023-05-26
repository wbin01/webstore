# import datetime
# import string
# import logging
#
# from django.shortcuts import get_object_or_404

import store.models as models


def get_favorite(request, product) -> models.ModelFavorite | None:
    """..."""
    try:
        return models.ModelFavorite.objects.filter(
            user=request.user.id).filter(product_id=product.id)
    except Exception as err:
        logging.error(err)
        return None


def get_favorite_list(request) -> list:
    """..."""
    try:
        favs = models.ModelFavorite.objects.filter(user=request.user)
    except Exception as err:
        logging.error(err)
        favs = []
    return favs
