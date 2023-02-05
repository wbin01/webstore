import datetime
import string
import logging
from django.shortcuts import get_object_or_404

import store.models as models


class GenericStoreProfile(object):
    def __init__(self) -> None:
        self.owner = None
        self.brand_name = 'Brand'
        self.show_brand_name_on_nav = True
        self.brand_image = None
        self.show_brand_image_on_nav = True
        self.theme_text_color = '#FFFFFF'
        self.theme_background_color = '#8A42AA'
        self.theme_admin_background_color = '#8F222D'
        self.social_media_facebook = None
        self.social_media_whatsapp = None
        self.social_media_twitter = None
        self.social_media_youtube = None
        self.social_media_instagram = None
        self.social_media_twitch = None
        self.social_media_discord = None
        self.social_media_linkedin = None
        self.social_media_github = None
        self.social_media_other = None


class GenericUserProfile(object):
    def __init__(self, request):
        self.user = request.user
        try:
            profile = get_object_or_404(
                models.ModelUserProfile, user=request.user.id)
        except Exception as err:
            profile = None
            logging.error(err)

        self.profile_image = profile.profile_image if profile else None
        self.is_admin = profile.is_admin if profile else False
        self.is_superuser = profile.is_superuser if profile else False


def get_cart(request, product) -> models.ModelProductCart | None:
    """..."""
    try:
        cart = models.ModelProductCart.objects.filter(
            user=request.user.id).filter(product_id=product.id)
        for item in cart:
            setattr(item, 'full_product', item.product)
    except Exception as err:
        logging.error(err)
        cart = None

    return cart


def get_cart_list(request):
    """..."""
    try:
        cart = models.ModelProductCart.objects.filter(user=request.user)
    except Exception as err:
        logging.error(err)
        cart = []
    return cart


def get_favorite(request, product) -> models.ModelFavorite | None:
    try:
        return models.ModelFavorite.objects.filter(
            user=request.user.id).filter(product_id=product.id)
    except Exception as err:
        logging.error(err)
        return None


def get_favorite_list(request):
    """..."""
    try:
        favs = models.ModelFavorite.objects.filter(user=request.user)
    except Exception as err:
        logging.error(err)
        favs = []
    return favs


def get_formatted_url_title(title: str) -> str:
    new_title = ''
    for char in title:
        char = char.lower()
        if char == ' ' or char in string.ascii_lowercase:
            new_title += char.replace(' ', '-')
    new_title = new_title.replace('--', '-')
    return new_title + datetime.datetime.now().strftime("%d-%m-%Y--%I-%M%p")


def get_store_profile() -> models.ModelUserProfile | GenericStoreProfile:
    """..."""
    try:
        profile = models.ModelStoreProfile.objects.all()
    except Exception as err:
        logging.error(err)
        profile = None

    if profile:
        return profile[0]
    return GenericStoreProfile()


def get_user_profile(request) -> models.ModelUserProfile | GenericUserProfile:
    """..."""
    try:
        return get_object_or_404(
            models.ModelUserProfile, user=request.user.id)
    except Exception as err:
        logging.error(err)
        return GenericUserProfile(request)


def format_card_title(title) -> str:
    """Product name"""
    if len(title) > 50:
        return title[:50] + '...'
    return title


def format_old_price(price_old) -> str:
    """R$ 0,00"""

    reais, cents = str(price_old).split('.')
    if len(cents) == 1:
        cents = f'{cents}0'

    return f'R$ {reais},{cents}'


def format_new_price(price) -> str:
    """R$ 0,00"""

    reais, cents = str(price).split('.')
    if len(cents) == 1:
        cents = f'{cents}0'

    return f'R$ {reais},{cents}'


def format_off_price(price, price_old) -> str | None:
    """10% OFF"""
    off = 0
    if price_old > price:
        delta_1 = price_old - price
        delta_2 = price_old / 100
        off = round(delta_1 / delta_2)

    if off > 4:
        return f'{off}% OFF'
    return None


def format_times_split_unit(
        price, times_split_num, times_split_interest) -> float | None:
    """5.00

    One unit extracted. If it is 10 times of 5.0, then it returns 5.0
    """
    if price:
        if times_split_num and times_split_num > 1:
            preco = price
            vezes = times_split_num
            juros = times_split_interest

            preco_real_com_juros = (preco / 100) * juros + preco
            preco = round((preco_real_com_juros / vezes), 2)

            return preco

    return None


def format_times_split_prices(    # times_split_pprint
        price, times_split_num, times_split_interest) -> str | None:
    """1x R$ 0,00"""
    if price:
        if times_split_num and times_split_num > 1:
            preco = format_times_split_unit(
                price, times_split_num, times_split_interest)
            reais, centavos = str(preco).split('.')

            if len(centavos) == 1:
                centavos = f'{centavos}0'

            return '{}x R$ {},{}'.format(
                times_split_num, reais, centavos)

    return None


def format_shipping_price(shipping_price) -> str | None:
    """Frete grátis"""
    if not shipping_price:
        return None
    reais, centavos = str(shipping_price).split('.')
    if len(centavos) == 1:
        centavos = f'{centavos}0'

    return 'R$ {},{}'.format(reais, centavos)


def format_max_quantity_per_sale(
        available_quantity, max_quantity_per_sale) -> int:
    """..."""
    if available_quantity < max_quantity_per_sale:
        return available_quantity
    return max_quantity_per_sale


def format_tags(tags) -> list:
    """[tag1, tag2, tag3]"""
    return [x.strip() for x in tags.split(',')]
