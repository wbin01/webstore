import logging
import string

from django.shortcuts import render
from store.models import ModelPost, ModelHighlightPosts, ModelStoreProfile


class Post(object):
    """..."""
    def __init__(self, post: ModelPost) -> None:
        """..."""
        self.post = post
        self.id = self.post.id
        self.user = self.post.user
        self.title = self.post.title
        self.url_title = self.__formatted_url_title()
        self.card_title = self.__formatted_card_title()
        self.old_price = self.__formatted_old_price()
        self.new_price = self.__formatted_new_price()
        self.off_price = self.__formatted_off_price()
        self.show_off_price = self.post.show_off_price
        self.times_split_num = self.post.times_split_num
        self.times_split_interest = self.post.times_split_interest
        self.times_split_value = self.__formatted_times_split_value()
        self.times_split_prices = self.__formatted_times_split_prices()
        self.shipping_price = self.__formatted_shipping_price()
        self.image_1 = self.post.image_1
        self.image_2 = self.post.image_2
        self.image_3 = self.post.image_3
        self.image_4 = self.post.image_4
        self.image_5 = self.post.image_5
        self.summary = self.post.summary
        self.content = self.post.content
        self.tags = self.__formatted_tags()
        self.publication_date = self.post.publication_date
        self.is_published = self.post.is_published

    def __formatted_url_title(self) -> str:
        title = ''
        for char in self.post.title:
            char = char.lower()
            if char == ' ' or char in string.ascii_lowercase:
                title += char.replace(' ', '-')
        return title.replace('--', '-')

    def __formatted_card_title(self) -> str:
        """Product name"""
        if len(self.post.title) > 50:
            return self.post.title[:50] + '...'
        return self.post.title

    def __formatted_old_price(self) -> str:
        """R$ 0,00"""

        reais, cents = str(self.post.old_price).split('.')
        if len(cents) == 1:
            cents = f'{cents}0'

        return f'R$ {reais},{cents}'

    def __formatted_new_price(self) -> str:
        """R$ 0,00"""

        reais, cents = str(self.post.new_price).split('.')
        if len(cents) == 1:
            cents = f'{cents}0'

        return f'R$ {reais},{cents}'

    def __formatted_off_price(self) -> str | None:
        """10% OFF"""
        off = 0
        if self.post.old_price > self.post.new_price:
            delta_1 = self.post.old_price - self.post.new_price
            delta_2 = self.post.old_price / 100
            off = round(delta_1 / delta_2)

        if off > 4:
            return f'{off}% OFF'
        return None

    def __formatted_times_split_value(self) -> float | None:
        """5.00

        One unit extracted. If it is 10 times of 5.0, then it returns 5.0
        """
        if self.post.new_price:
            if self.post.times_split_num and self.post.times_split_num > 1:
                preco = self.post.new_price
                vezes = self.post.times_split_num
                juros = self.post.times_split_interest

                preco_real_com_juros = (preco / 100) * juros + preco
                preco = round((preco_real_com_juros / vezes), 2)

                return preco

        return None

    def __formatted_times_split_prices(self) -> str | None:
        """1x R$ 0,00"""
        if self.post.new_price:
            if self.post.times_split_num and self.post.times_split_num > 1:
                preco = self.__formatted_times_split_value()
                reais, centavos = str(preco).split('.')

                if len(centavos) == 1:
                    centavos = f'{centavos}0'

                return '{}x R$ {},{}'.format(
                    self.post.times_split_num, reais, centavos)

        return None

    def __formatted_shipping_price(self) -> str | None:
        """Frete grátis"""
        if not self.post.shipping_price:
            return None
        reais, centavos = str(self.post.shipping_price).split('.')
        if len(centavos) == 1:
            centavos = f'{centavos}0'

        return 'R$ {},{}'.format(reais, centavos)

    def __formatted_tags(self) -> list:
        """[tag1, tag2, tag3]"""
        return [x.strip() for x in self.post.tags.split(',')]


def store_context():
    return {'store_name': 'lol'}


def index(request):
    posts = (
        ModelPost.objects.order_by('-publication_date')
        .filter(is_published=True))
    highlight_posts = ModelHighlightPosts.objects.all()

    context = {
        'store_profile': ModelStoreProfile.objects.all()[0],
        'posts': [Post(x) for x in posts],
        'highlight_posts': highlight_posts}

    if not request.user.is_authenticated:
        return render(request, 'index.html', context)
    return render(request, 'index.html', context)


def signup(request):
    context = {}
    if not request.user.is_authenticated:
        return render(request, 'signup.html', context)
    return render(request, 'index.html', context)


def login(request):
    context = {}
    if not request.user.is_authenticated:
        return render(request, 'login.html', context)
    return render(request, 'index.html', context)


def logout(request):
    context = {}
    if request.user.is_authenticated:
        return render(request, 'logout.html', context)
    return render(request, 'index.html', context)


def product(request, url_title, post_id):
    logging.info(url_title)
    context = {
        'store_profile': ModelStoreProfile.objects.all()[0],
        'post': Post(ModelPost.objects.get(pk=post_id))}

    if not request.user.is_authenticated:
        return render(request, 'product.html', context)
    return render(request, 'index.html', context)


def search(request):
    search_text = request.GET['q']
    posts = (ModelPost.objects.order_by(
        '-publication_date').filter(is_published=True).filter(
        title__icontains=search_text) if search_text else [])

    context = {
        'store_profile': ModelStoreProfile.objects.all()[0],
        'search_text': search_text,
        'posts': [Post(x) for x in posts]}

    if not request.user.is_authenticated:
        return render(request, 'search.html', context)
    return render(request, 'index.html', context)


def search_tag(request):
    search_text = request.GET['q']
    posts = (ModelPost.objects.order_by(
        '-publication_date').filter(is_published=True).filter(
        tags__icontains=search_text) if search_text else [])

    context = {
        'store_profile': ModelStoreProfile.objects.all()[0],
        'search_text': search_text,
        'posts': [Post(x) for x in posts]}

    if not request.user.is_authenticated:
        return render(request, 'search_tag.html', context)
    return render(request, 'index.html', context)
