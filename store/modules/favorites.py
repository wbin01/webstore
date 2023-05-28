import logging

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


def remove_from_favorites(request):
    favorite_item = get_favorite(
        request, models.ModelProduct.objects.get(
            pk=request.POST['remove_from_favorites']))
    if favorite_item:
        favorite_item.delete()
