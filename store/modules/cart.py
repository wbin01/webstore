import logging

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

import store.models as models
import store.modules.favorites as mdl_favorites
import store.modules.value_convert as mdl_value_convert


def add_to_favorites(request):
    favorite_item = models.ModelFavorite.objects.create(
        user=get_object_or_404(User, pk=request.user.id),
        product=models.ModelProduct.objects.get(
            pk=request.POST['add_to_favorites']))
    favorite_item.save()


def edit_item(request):
    cart_item = models.ModelCart.objects.get(pk=request.POST['edit_item'])
    cart_product = models.ModelProduct.objects.get(pk=cart_item.product.id)

    quantity = int(request.POST['quantity'])
    cart_item.quantity = quantity

    times_split_num = int(request.POST['times_split_num'])
    cart_item.times_split_num = times_split_num

    times_split_unit = edit_split_unit(
        cart_product.price,
        quantity,
        times_split_num,
        cart_product.times_split_interest)
    cart_item.times_split_unit = times_split_unit

    cart_item.times_split_pprint = edit_split_pprint(
        times_split_num,
        times_split_unit)

    total_prices = edit_total_price(
        cart_product.price,
        quantity,
        cart_product.times_split_interest,
        times_split_num)
    cart_item.total_price = total_prices

    cart_item.total_price_pprint = edit_total_price_pprint(
        total_prices)

    cart_item.save()


def edit_split_pprint(split_num, split_unit) -> str:
    """..."""
    price = mdl_value_convert.value_pprint(float(split_unit))
    return '{}x {}'.format(split_num, price)


def edit_split_unit(price, quantity, split_num, split_interest) -> float:
    """5.00

    One unit extracted. If it is 10 times of 5.0, then it returns 5.0
    """
    preco = float(price)
    quantity = int(quantity)
    preco = round(preco * quantity, 2)
    vezes = int(split_num)
    juros = int(split_interest)
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


def edit_total_price(
        price: float, quantity: int, split_gain: int, split_num: int) -> float:
    """..."""
    if price > 0.0:
        if split_num == 1:
            return price * quantity

        if split_num > 1 and not split_gain:
            return price * quantity

        if split_num > 1 and split_gain:
            interest = round(price / 100, 2) * split_gain
            price += interest
            return price * quantity
    return 0.0


def edit_total_price_pprint(price: float) -> str:
    """..."""
    return mdl_value_convert.value_pprint(price)


def item(request, product) -> models.ModelCart | None:
    """..."""
    try:
        cart = models.ModelCart.objects.filter(
            user=request.user.id).filter(product_id=product.id)
        for cart_item in cart:
            setattr(cart_item, 'full_product', cart_item.product)
    except Exception as err:
        logging.error(err)
        cart = None

    return cart


def items_list(request) -> list:
    """..."""
    try:
        cart = models.ModelCart.objects.filter(user=request.user)
    except Exception as err:
        logging.error(err)
        cart = []
    return cart


def new_item(user_id, model_product) -> None:
    cart_item = models.ModelCart.objects.create(
        user=get_object_or_404(User, pk=user_id),
        product=model_product,
        times_split_num=1,
        times_split_unit=model_product.price,
        times_split_pprint='1x ' + model_product.price_pprint,
        quantity=1,
        total_price=model_product.price,
        total_price_pprint=model_product.price_pprint)
    cart_item.save()


def remove_from_favorites(request):
    favorite_item = mdl_favorites.item(
        request, models.ModelProduct.objects.get(
            pk=request.POST['remove_from_favorites']))
    if favorite_item:
        favorite_item.delete()


def remove_item(request):
    model_product = models.ModelProduct.objects.get(
        pk=request.POST['remove_item'])
    cart_item = item(request, model_product)
    cart_item.delete()


def total_price(cart_list):
    """..."""
    if not cart_list:
        return 0.0

    total = 0.0
    for cart in cart_list:
        total += cart.total_price
    # return round(total + mdl_total_price.total_shipping_price(cart_list), 2)
    return round(total + total_price_with_shipping(cart_list), 2)


def total_price_pprint(total):
    """..."""
    return mdl_value_convert.value_pprint(float(total))


def total_price_split_list(cart_list) -> dict:
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


def total_price_split_list_pprint(total_prices_split_list) -> dict:
    """..."""
    split_price = {}
    for key, value in total_prices_split_list.items():
        split_price[key + 1] = mdl_value_convert.value_pprint(float(value))

    return split_price


def total_price_with_shipping(cart_list):
    """..."""
    if not cart_list:
        return 0.0

    shipping = 0.0
    for cart_item in cart_list:
        if cart_item.product.shipping_price > shipping:
            shipping = cart_item.product.shipping_price
    return shipping


def total_price_with_shipping_pprint(price):
    """..."""
    return mdl_value_convert.value_pprint(float(price))
