import logging
import string

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth

from store.models import (
    ModelPost, ModelHighlightPosts, ModelStoreProfile, ModelUserProfile)
from store.forms import FormLogin, FormSignup

import store.validation as validation


class StoreProfile(object):
    def __init__(self) -> None:
        self.owner = None
        self.brand_name = 'Brand'
        self.show_brand_name_on_nav = True
        self.brand_image = None
        self.show_brand_image_on_nav = True
        self.theme_text_color = '#FFFFFF'
        self.theme_background_color = '#8A42AA'
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


def index(request):
    highlight_posts = ModelHighlightPosts.objects.all()
    store_profile = ModelStoreProfile.objects.all()
    posts = (
        ModelPost.objects.order_by('-publication_date')
        .filter(is_published=True))
    context = {
        'store_profile': store_profile[0] if store_profile else StoreProfile(),
        'user_profile': None,
        'posts': [Post(x) for x in posts],
        'highlight_posts': highlight_posts}

    if request.user.is_authenticated:
        try:
            profile = get_object_or_404(ModelUserProfile, user=request.user.id)
            context['user_profile'] = profile
        except Exception as err:
            logging.error(err)

    return render(request, 'index.html', context)


def signup(request):
    if request.user.is_authenticated:
        return redirect('index')

    store_profile = ModelStoreProfile.objects.all()
    context = {
        'store_profile': store_profile[0] if store_profile else StoreProfile(),
        'user_profile': None,
        'form': FormSignup,
        'signup_status': None}

    if not request.user.is_authenticated:
        if request.method != 'POST':
            return render(request, 'signup.html', context)

        if request.method == 'POST':
            name = request.POST['name']
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            password_confirm = request.POST['password_confirm']

            space_err = validation.invalid_whitespace(
                [name, username, email, password, password_confirm])
            if space_err:
                context['signup_status'] = space_err

            username_err = validation.invalid_username(username)
            if username_err:
                context['signup_status'] = username_err

            email_err = validation.invalid_email(email)
            if email_err:
                context['signup_status'] = email_err

            pass_err = validation.invalid_password(password, password_confirm)
            if pass_err:
                context['signup_status'] = pass_err

            if User.objects.filter(username=email).exists():
                context['signup_status'] = 'Usuário já cadastrado'

            if User.objects.filter(email=email).exists():
                context['signup_status'] = 'Email já cadastrado'

            if context['signup_status']:
                return render(request, 'signup.html', context)

            user = User.objects.create_user(
                username=username, first_name=name,
                email=email, password=password)
            user.save()

            profile = ModelUserProfile.objects.create(
                user=get_object_or_404(User, pk=user.id),
                is_admin=False,
                is_superuser=False)
            profile.save()

            return redirect('login')


def login(request):
    store_profile = ModelStoreProfile.objects.all()
    context = {
        'store_profile': store_profile[0] if store_profile else StoreProfile(),
        'user_profile': None,
        'form': FormLogin,
        'login_status': None}

    if request.user.is_authenticated:
        return redirect('index')

    if not request.user.is_authenticated:
        if request.method != 'POST':
            return render(request, 'login.html', context)

        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            if not User.objects.filter(username=username).exists():
                context['login_status'] = 'Usuário ou senha incorreto'
                return render(request, 'login.html', context)

            if User.objects.filter(username=username).exists():
                user = auth.authenticate(
                    request, username=username, password=password)

                if not user:
                    context['login_status'] = 'Usuário ou senha incorreto'
                    return render(request, 'login.html', context)

                if user:
                    auth.login(request, user)
                    return redirect('index')


def logout(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            auth.logout(request)

    return redirect('index')


def product(request, url_title, post_id):
    logging.info(url_title)
    store_profile = ModelStoreProfile.objects.all()
    context = {
        'store_profile': store_profile[0] if store_profile else StoreProfile(),
        'post': Post(ModelPost.objects.get(pk=post_id)),
        'user_profile': None}

    if request.user.is_authenticated:
        try:
            profile = get_object_or_404(ModelUserProfile, user=request.user.id)
            context['user_profile'] = profile
            print('XXXXXXXX', profile.profile_image.url)
        except Exception as err:
            logging.error(err)

    return render(request, 'product.html', context)


def search(request):
    search_text = request.GET['q']
    posts = (ModelPost.objects.order_by(
        '-publication_date').filter(is_published=True).filter(
        title__icontains=search_text) if search_text else [])

    store_profile = ModelStoreProfile.objects.all()
    context = {
        'store_profile': store_profile[0] if store_profile else StoreProfile(),
        'user_profile': None,
        'search_text': search_text,
        'posts': [Post(x) for x in posts]}

    if request.user.is_authenticated:
        try:
            profile = get_object_or_404(ModelUserProfile, user=request.user.id)
            context['user_profile'] = profile
        except Exception as err:
            logging.error(err)

    return render(request, 'search.html', context)


def search_tag(request):
    search_text = request.GET['q']
    posts = (ModelPost.objects.order_by(
        '-publication_date').filter(is_published=True).filter(
        tags__icontains=search_text) if search_text else [])

    store_profile = ModelStoreProfile.objects.all()
    context = {
        'store_profile': store_profile[0] if store_profile else StoreProfile(),
        'user_profile': None,
        'search_text': search_text,
        'posts': [Post(x) for x in posts]}

    if request.user.is_authenticated:
        try:
            profile = get_object_or_404(ModelUserProfile, user=request.user.id)
            context['user_profile'] = profile
        except Exception as err:
            logging.error(err)

    return render(request, 'search_tag.html', context)
