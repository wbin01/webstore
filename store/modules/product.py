import datetime
import json
import string

from django.utils import timezone

import store.models as models
from store.modules.value_convert import value_pprint
import store.modules.validations as mdl_validations


def card_title(title: str) -> str:
    """Short product title"""
    if len(title) > 50:
        return title[:50] + '...'
    return title


def edition_warnings(request) -> str | None:
    warning = None
    for image in ['image_1', 'image_2', 'image_3', 'image_4', 'image_5']:
        if image in request.FILES:
            warning = mdl_validations.invalid_image(request.FILES[image])
            if warning:
                break
    return warning


def max_quantity_per_sale(available_quantity: str, max_quantity: str) -> int:
    """..."""
    available_quantity = int(available_quantity)
    max_quantity = int(max_quantity)
    if available_quantity < max_quantity:
        return available_quantity
    return max_quantity


def price_off(price: str, price_old: str) -> float:
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


def price_off_pprint(price: str, price_old: str) -> str:
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


def price_pprint(price: str) -> str:
    """R$ 0,00"""
    return value_pprint(float(price))


def save_edition(request, product_id) -> None:
    editable = models.ModelProduct.objects.get(pk=product_id)
    if 'title' in request.POST:
        editable.title = request.POST['title']
        editable.title_for_card = card_title(request.POST['title'])
    if 'price' in request.POST:
        editable.price_old = editable.price
        editable.price_old_pprint = price_pprint(str(editable.price))
        editable.price = float(request.POST['price'])
        editable.price_pprint = price_pprint(request.POST['price'])
        editable.price_off = price_off(
            request.POST['price'], str(editable.price_old))
        editable.price_off_pprint = price_off_pprint(
            request.POST['price'], str(editable.price_old))
    if 'times_split_num' in request.POST:
        editable.times_split_num = int(request.POST['times_split_num'])
    if 'times_split_interest' in request.POST:
        editable.times_split_interest = int(
            request.POST['times_split_interest'])
    if 'shipping_price' in request.POST:
        editable.shipping_price = float(request.POST['shipping_price'])
        editable.shipping_price_pprint = (
            shipping_price_pprint(request.POST['shipping_price']))
    if 'available_quantity' in request.POST:
        editable.available_quantity = int(request.POST['available_quantity'])
    if 'max_quantity_per_sale' in request.POST:
        editable.max_quantity_per_sale = max_quantity_per_sale(
            request.POST['available_quantity'],
            request.POST['max_quantity_per_sale'])

    if 'image_1' in request.FILES:
        editable.image_1 = request.FILES['image_1']

    remove_image_2 = True if 'remove_image_2' in request.POST else False
    if remove_image_2:
        editable.image_2 = None
    else:
        if 'image_2' in request.FILES:
            editable.image_2 = request.FILES['image_2']

    remove_image_3 = True if 'remove_image_3' in request.POST else False
    if remove_image_3:
        editable.image_3 = None
    else:
        if 'image_3' in request.FILES:
            editable.image_3 = request.FILES['image_3']

    remove_image_4 = True if 'remove_image_4' in request.POST else False
    if remove_image_4:
        editable.image_4 = None
    else:
        if 'image_4' in request.FILES:
            editable.image_4 = request.FILES['image_4']

    remove_image_5 = True if 'remove_image_5' in request.POST else False
    if remove_image_5:
        editable.image_5 = None
    else:
        if 'image_5' in request.FILES:
            editable.image_5 = request.FILES['image_5']

    if 'summary' in request.POST:
        editable.summary = request.POST['summary']

    if 'content' in request.POST:
        content_text = request.POST['content']
        content_text = json.loads(content_text)['html'] if content_text else ''
        editable.content = content_text

    if 'tags' in request.POST:
        editable.tags = request.POST['tags']
    if ('price' not in request.POST or
            'times_split_num' not in request.POST or
            'times_split_interest' not in request.POST):
        context['product_status'] = 'há campos vazios'
    else:
        editable.times_split_unit = split_unit(
            request.POST['price'],
            request.POST['times_split_num'],
            request.POST['times_split_interest'])
        editable.times_split_pprint = split_pprint(
            request.POST['price'],
            request.POST['times_split_num'],
            request.POST['times_split_interest'])
    editable.publication_date = timezone.now()
    editable.price_off_display = (
        True if 'price_off_display' in request.POST else False)
    editable.available_quantity_display = (
        True if 'available_quantity_display' in request.POST else False)
    editable.is_published = (
        True if 'is_published' in request.POST else False)

    editable.save()


def shipping_price_pprint(shipping_price) -> str:
    """Frete grátis"""
    if not shipping_price:
        return ''
    return value_pprint(float(shipping_price))


def split_unit(price, split_num, split_gain) -> float:
    """5.00

    One unit extracted. If it is 10 times of 5.0, then it returns 5.0
    """
    preco = float(price)
    vezes = int(split_num)
    juros = int(split_gain)
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


def split_pprint(price, split_num, split_gain) -> str:
    """1x R$ 0,00"""
    if float(price) > 0.0:
        if int(split_num) and int(split_num) > 1:
            preco = split_unit(price, split_num, split_gain)
            return '{}x {}'.format(split_num, value_pprint(float(preco)))
    return ''


def tags(tag: str) -> list:
    """[tag1, tag2, tag3]"""
    return [x.strip() for x in tag.split(',')]


def url_title(title: str) -> str:
    """the-title"""
    new_title = ''
    for char in title:
        char = char.lower()
        if char == ' ' or char in string.ascii_lowercase:
            new_title += char.replace(' ', '-')
    new_title = new_title.replace('--', '-')
    return new_title + datetime.datetime.now().strftime("%d-%m-%Y--%I-%M%p")
