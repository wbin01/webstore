def value_pprint(value: float, hide_sign: bool = False) -> str:
    """Money in pprint format

    10,00
    100,30
    1.000,50
    """
    dollar, cents = str(value).split('.')
    return '{}{},{}'.format(
        '' if hide_sign else 'R$ ',
        reais_pprint(dollar), cents_pprint(cents))


def reais_pprint(real: str) -> str:
    """..."""
    if len(real) > 3:
        real = '{}.{}'.format(real[:-3], real[-3:])
    return real


def cents_pprint(cent: str) -> str:
    """..."""
    if len(cent) == 1:
        cent = f'{cent}0'
    return cent
