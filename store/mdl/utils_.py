import datetime
import string
import logging
from django.shortcuts import get_object_or_404

import store.models as models


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
    """..."""
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


def get_store_profile() -> models.ModelStoreProfile:
    """..."""
    try:
        profile = models.ModelStoreProfile.objects.all()
    except Exception as err:
        logging.error(err)
        profile = None

    if not profile:
        profile = models.ModelStoreProfile.objects.create(
            brand_name='Brand',
            show_brand_name_on_nav=True,
            brand_image=None,
            show_brand_image_on_nav=True,
            background_color='#ECECEC',
            theme_color='#8A42AA',
            theme_color_admin='#8F222D',
            theme_color_text='#FFFFFF',
            social_media_facebook=None,
            social_media_whatsapp=None,
            social_media_twitter=None,
            social_media_youtube=None,
            social_media_instagram=None,
            social_media_twitch=None,
            social_media_discord=None,
            social_media_linkedin=None,
            social_media_github=None,
            social_media_other=None)
        profile.save()

    profile = models.ModelStoreProfile.objects.all()
    return profile[0]


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
    return money_pprint(float(price))


def product_price_off(price: str, price_old: str) -> float:
    """10 -> 10% OFF"""
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
        if vezes == 1:
            return preco
        if vezes > 1 and juros == 0:
            preco = round((preco / vezes), 2)
            return preco
        if vezes > 1 and juros > 1:
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
            return '{}x {}'.format(times_split_num, money_pprint(float(preco)))

    return ''


def product_shipping_price_pprint(shipping_price) -> str:
    """Frete grátis"""
    if not shipping_price:
        return ''
    return money_pprint(float(shipping_price))


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
    """..."""
    if not cart_list:
        return 0.0

    shipping = 0.0
    for item in cart_list:
        if item.product.shipping_price > shipping:
            shipping = item.product.shipping_price
    return shipping


def total_shipping_price_pprint(price):
    """..."""
    return money_pprint(float(price))


def cart_edit_times_split_unit(
        price, quantity, times_split_num, times_split_interest) -> float:
    """5.00

    One unit extracted. If it is 10 times of 5.0, then it returns 5.0
    """
    preco = float(price)
    quantity = int(quantity)
    preco = round(preco * quantity, 2)
    vezes = int(times_split_num)
    juros = int(times_split_interest)
    if preco > 0.0:
        if vezes == 1:
            return preco
        if vezes > 1 and juros == 0:
            preco = round((preco / vezes), 2)
            return preco
        if vezes > 1 and juros > 1:
            preco_real_com_juros = (preco / 100) * juros + preco
            preco = round((preco_real_com_juros / vezes), 2)
            return preco
    return 0.0


def cart_edit_times_split_pprint(
        times_split_num, times_split_unit) -> str:
    """..."""
    price = money_pprint(float(times_split_unit))
    return '{}x {}'.format(times_split_num, price)


def cart_edit_total_price(
        price: float,
        quantity: int,
        times_split_interest: int,
        times_split_num: int) -> float:
    """..."""
    if price > 0.0:
        if times_split_num == 1:
            return price * quantity

        if times_split_num > 1 and not times_split_interest:
            return price * quantity

        if times_split_num > 1 and times_split_interest:
            interest = round(price / 100, 2) * times_split_interest
            price += interest
            return price * quantity
    return 0.0


def cart_edit_total_price_pprint(price: float) -> str:
    """..."""
    return money_pprint(price)


def cart_total_price(cart_list):
    """..."""
    if not cart_list:
        return 0.0

    total = 0.0
    for cart in cart_list:
        total += cart.total_price
    return round(total + total_shipping_price(cart_list), 2)


def cart_total_price_split_list(cart_list) -> dict:
    """..."""
    split_price = {0: 0.0}
    for cart in cart_list:
        for i in range(cart.times_split_num):
            if i in split_price.keys():
                split_price[i] = split_price[i] + cart.times_split_unit
            else:
                split_price[i] = cart.times_split_unit
    return split_price


def cart_total_price_split_list_pprint(total_price_split_list) -> dict:
    """..."""
    split_price = {}
    for key, value in total_price_split_list.items():
        split_price[key + 1] = money_pprint(float(value))

    return split_price


def cart_total_price_pprint(total):
    """..."""
    return money_pprint(float(total))


def money_pprint(value: float, hide_sign: bool = False) -> str:
    """Money in pprint format

    10,00
    100,30
    1.000,50
    """
    dollar, cents = str(value).split('.')
    return '{}{},{}'.format(
        '' if hide_sign else 'R$ ',
        money_dollar_pprint(dollar), money_cents_pprint(cents))


def money_dollar_pprint(real: str) -> str:
    """..."""
    if len(real) > 3:
        real = '{}.{}'.format(real[:-3], real[-3:])
    return real


def money_cents_pprint(cent: str) -> str:
    """..."""
    if len(cent) == 1:
        cent = f'{cent}0'
    return cent
