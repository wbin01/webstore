import datetime
import string
# import logging
#
# from django.shortcuts import get_object_or_404
#
# import store.models as models


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
