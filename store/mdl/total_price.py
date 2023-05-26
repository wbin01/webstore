# import datetime
# import string
# import logging
#
# from django.shortcuts import get_object_or_404
#
# import store.models as models

from pprint_format_money import money_pprint


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
