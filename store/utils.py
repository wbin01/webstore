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
        self.background_color = '#ECECEC'
        self.theme_color = '#8A42AA'
        self.theme_color_admin = '#8F222D'
        self.theme_color_text = '#FFFFFF'
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


def get_cart(request, product) -> models.ModelCart | None:
    """..."""
    try:
        cart = models.ModelCart.objects.filter(
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
        cart = models.ModelCart.objects.filter(user=request.user)
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


def product_title_for_url(title: str) -> str:
    """the-title"""
    new_title = ''
    for char in title:
        char = char.lower()
        if char == ' ' or char in string.ascii_lowercase:
            new_title += char.replace(' ', '-')
    new_title = new_title.replace('--', '-')
    return new_title + datetime.datetime.now().strftime("%d-%m-%Y--%I-%M%p")


def product_title_for_card(title: str) -> str:
    """Short product title"""
    if len(title) > 50:
        return title[:50] + '...'
    return title


def product_price_pprint(price: str) -> str:
    """R$ 0,00"""

    reais, cents = str(float(price)).split('.')
    if len(cents) == 1:
        cents = f'{cents}0'

    return f'R$ {reais},{cents}'


def product_price_off(price: str, price_old: str) -> float:
    """10% OFF"""
    price, price_old = float(price), float(price_old)
    off = 0
    if price_old > price:
        delta_1 = price_old - price
        delta_2 = price_old / 100
        off = round(delta_1 / delta_2)

    if off > 4:
        return off
    return 0.0


def product_price_off_pprint(price: str, price_old: str) -> str:
    """10% OFF"""
    price, price_old = float(price), float(price_old)
    off = 0
    if price_old > price:
        delta_1 = price_old - price
        delta_2 = price_old / 100
        off = round(delta_1 / delta_2)

    if off > 4:
        return f'{off}% OFF'
    return 'R$ 0.00% OFF'


def product_times_split_unit(
        price, times_split_num, times_split_interest) -> float:
    """5.00

    One unit extracted. If it is 10 times of 5.0, then it returns 5.0
    """
    preco = float(price)
    vezes = int(times_split_num)
    juros = int(times_split_interest)
    if preco > 0.0:
        if vezes and juros > 1:
            preco_real_com_juros = (preco / 100) * juros + preco
            preco = round((preco_real_com_juros / vezes), 2)
            return preco
    return 0.0


def product_times_split_pprint(
        price, times_split_num, times_split_interest) -> str:
    """1x R$ 0,00"""

    if float(price) > 0.0:
        if int(times_split_num) and int(times_split_num) > 1:
            preco = product_times_split_unit(
                price, times_split_num, times_split_interest)
            reais, centavos = str(float(preco)).split('.')

            if len(centavos) == 1:
                centavos = f'{centavos}0'

            return '{}x R$ {},{}'.format(
                times_split_num, reais, centavos)

    return ''


def product_shipping_price_pprint(shipping_price) -> str:
    """Frete grátis"""
    if not shipping_price:
        return ''
    reais, centavos = str(float(shipping_price)).split('.')
    if len(centavos) == 1:
        centavos = f'{centavos}0'

    return 'R$ {},{}'.format(reais, centavos)


def product_max_quantity_per_sale(
        available_quantity: str, max_quantity_per_sale: str) -> int:
    """..."""
    available_quantity = int(available_quantity)
    max_quantity_per_sale = int(max_quantity_per_sale)
    if available_quantity < max_quantity_per_sale:
        return available_quantity
    return max_quantity_per_sale


def product_tags(tags: str) -> list:
    """[tag1, tag2, tag3]"""
    return [x.strip() for x in tags.split(',')]


def total_shipping_price(cart_list):
    if not cart_list:
        return 0.0

    shipping = 0.0
    for item in cart_list:
        if item.product.shipping_price > shipping:
            shipping = item.product.shipping_price
    return shipping


def total_shipping_price_pprint(price):
    reais, centavos = str(price).split('.')

    if len(centavos) == 1:
        centavos = f'{centavos}0'

    return 'R$ {},{}'.format(reais, centavos)


def total_price(cart_list):
    if not cart_list:
        return 0.0

    total = 0.0
    for cart in cart_list:
        total += cart.product.price
    return round(total + total_shipping_price(cart_list), 2)


def total_price_pprint(total):
    reais, centavos = str(total).split('.')

    if len(centavos) == 1:
        centavos = f'{centavos}0'

    return 'R$ {},{}'.format(reais, centavos)
