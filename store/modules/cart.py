import logging

from django.shortcuts import get_object_or_404  # render, redirect
from django.contrib.auth.models import User

import store.models as models
import store.modules.favorites as mdl_favorites
import store.modules.pprint_values as mdl_pprint_values
import store.modules.total_price as mdl_total_price


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


def get_cart_list(request) -> list:
    """..."""
    try:
        cart = models.ModelCart.objects.filter(user=request.user)
    except Exception as err:
        logging.error(err)
        cart = []
    return cart


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
    price = mdl_pprint_values.money_pprint(float(times_split_unit))
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
    return mdl_pprint_values.money_pprint(price)


def cart_total_price(cart_list):
    """..."""
    if not cart_list:
        return 0.0

    total = 0.0
    for cart in cart_list:
        total += cart.total_price
    return round(total + mdl_total_price.total_shipping_price(cart_list), 2)


def cart_total_price_split_list(cart_list) -> dict:
    """..."""
    split_price = {0: 0.0}
    for cart in cart_list:
        for i in range(cart.times_split_num):
            if i in split_price.keys():
                split_price[i] = round(
                    split_price[i] + cart.times_split_unit, 2)
            else:
                split_price[i] = cart.times_split_unit
    return split_price


def cart_total_price_split_list_pprint(total_price_split_list) -> dict:
    """..."""
    split_price = {}
    for key, value in total_price_split_list.items():
        split_price[key + 1] = mdl_pprint_values.money_pprint(float(value))

    return split_price


def cart_total_price_pprint(total):
    """..."""
    return mdl_pprint_values.money_pprint(float(total))


def edit_item(request):
    cart_item = models.ModelCart.objects.get(pk=request.POST['edit_item'])
    cart_product = models.ModelProduct.objects.get(pk=cart_item.product.id)

    quantity = int(request.POST['quantity'])
    cart_item.quantity = quantity

    times_split_num = int(request.POST['times_split_num'])
    cart_item.times_split_num = times_split_num

    times_split_unit = cart_edit_times_split_unit(
        cart_product.price,
        quantity,
        times_split_num,
        cart_product.times_split_interest)
    cart_item.times_split_unit = times_split_unit

    cart_item.times_split_pprint = cart_edit_times_split_pprint(
        times_split_num,
        times_split_unit)

    total_price = cart_edit_total_price(
        cart_product.price,
        quantity,
        cart_product.times_split_interest,
        times_split_num)
    cart_item.total_price = total_price

    cart_item.total_price_pprint = cart_edit_total_price_pprint(
        total_price)

    cart_item.save()


def remove_item(request):
    model_product = models.ModelProduct.objects.get(
        pk=request.POST['remove_item'])
    cart_item = get_cart(request, model_product)
    cart_item.delete()


def add_to_favorites(request):
    favorite_item = models.ModelFavorite.objects.create(
        user=get_object_or_404(User, pk=request.user.id),
        product=models.ModelProduct.objects.get(
            pk=request.POST['add_to_favorites']))
    favorite_item.save()


def remove_from_favorites(request):
    favorite_item = mdl_favorites.get_favorite(
        request, models.ModelProduct.objects.get(
            pk=request.POST['remove_from_favorites']))
    if favorite_item:
        favorite_item.delete()