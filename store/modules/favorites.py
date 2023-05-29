import logging

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

import store.models as models


def item(request, product) -> models.ModelFavorite | None:
    """..."""
    try:
        return models.ModelFavorite.objects.filter(
            user=request.user.id).filter(product_id=product.id)
    except Exception as err:
        logging.error(err)
        return None


def items_list(request) -> list:
    """..."""
    try:
        favs = models.ModelFavorite.objects.filter(user=request.user)
    except Exception as err:
        logging.error(err)
        favs = []
    return favs


def remove_item(request):
    favorite_item = item(
        request, models.ModelProduct.objects.get(
            pk=request.POST['remove_from_favorites']))
    if favorite_item:
        favorite_item.delete()


def new_item(user_id, model_product) -> None:
    fav = models.ModelFavorite.objects.create(
        user=get_object_or_404(User, pk=user_id),
        product=model_product)
    fav.save()
