# import datetime
# import string
# import logging
#
# from django.shortcuts import get_object_or_404
#
# import store.models as models


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
