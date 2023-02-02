import logging
import string

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth

from store.models import (
    ModelBuy, ModelCart, ModelFavorite, ModelHighlightPosts, ModelProduct,
    ModelStoreProfile, ModelUserProfile)
from store.forms import FormLogin, FormSignup

import store.validation as validation
from store.model_support import StoreProfile, ProductProfile, UserProfile


def cart_request(request, product_id):
    product_ = ProductProfile(ModelProduct.objects.get(pk=product_id))

    try:
        cart = ModelCart.objects.filter(user=request.user.id).filter(
            product_id=product_.id)
    except Exception as err:
        cart = None
        logging.error(err)

    if cart:
        cart.delete()
    else:
        cart = ModelCart.objects.create(
            user=get_object_or_404(User, pk=request.user.id),
            product_id=int(product_.id),
            product_title=product_.title)
        cart.save()

    return redirect('product', product_.url_title, product_.id)


def favorite_request(request, product_id):
    product_ = ProductProfile(ModelProduct.objects.get(pk=product_id))

    try:
        favorite = ModelFavorite.objects.filter(user=request.user.id).filter(
            product_id=product_.id)
    except Exception as err:
        favorite = None
        logging.error(err)

    if favorite:
        favorite.delete()
    else:
        favorite = ModelFavorite.objects.create(
            user=get_object_or_404(User, pk=request.user.id),
            product_id=int(product_.id),
            product_title=product_.title)
        favorite.save()

    return redirect('product', product_.url_title, product_.id)


def index(request):
    highlight_posts = ModelHighlightPosts.objects.all()
    store_profile = ModelStoreProfile.objects.all()
    posts = (
        ModelProduct.objects.order_by('-publication_date')
        .filter(is_published=True))
    context = {
        'store_profile': store_profile[0] if store_profile else StoreProfile(),
        'user_profile': None,
        'products': [ProductProfile(x) for x in posts],
        'highlight_posts': highlight_posts}

    if not request.user.is_authenticated:
        return render(request, 'index_for_visitors.html', context)

    if request.user.is_authenticated:
        profile = UserProfile(request)
        context['user_profile'] = profile if profile else UserProfile(request)

        if not profile.is_admin:
            return render(request, 'index_for_users.html', context)

        if profile.is_admin:
            return render(request, 'index_for_admins.html', context)


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


def product(request, product_url_title, product_id):
    logging.info(product_url_title)
    store_profile = ModelStoreProfile.objects.all()
    product_rofile = ProductProfile(ModelProduct.objects.get(pk=product_id))

    context = {
        'store_profile': store_profile[0] if store_profile else StoreProfile(),
        'product': product_rofile,
        'favorite': None,
        'cart': None,
        'user_profile': None}

    if not request.user.is_authenticated:
        return render(request, 'product_for_visitors.html', context)

    if request.user.is_authenticated:
        profile = UserProfile(request)
        context['user_profile'] = profile if profile else UserProfile(request)

        try:
            context['favorite'] = ModelFavorite.objects.filter(
                user=request.user.id).filter(product_id=product_rofile.id)
        except Exception as err:
            logging.error(err)
            context['favorite'] = None

        try:
            context['cart'] = ModelCart.objects.filter(
                user=request.user.id).filter(product_id=product_rofile.id)
        except Exception as err:
            logging.error(err)
            context['cart'] = None

        if not profile.is_admin and not profile.is_superuser:
            return render(request, 'product_for_users.html', context)

        if profile.is_admin or profile.is_superuser:
            return render(request, 'product_for_admins.html', context)


def search(request):
    search_text = request.GET['q']
    posts = (ModelProduct.objects.order_by(
        '-publication_date').filter(is_published=True).filter(
        title__icontains=search_text) if search_text else [])

    store_profile = ModelStoreProfile.objects.all()
    context = {
        'store_profile': store_profile[0] if store_profile else StoreProfile(),
        'user_profile': None,
        'search_text': search_text,
        'posts': [ProductProfile(x) for x in posts]}

    if request.user.is_authenticated:
        profile = UserProfile(request)
        context['user_profile'] = profile if profile else UserProfile(request)

    return render(request, 'search.html', context)


def search_tag(request):
    search_text = request.GET['q']
    posts = (ModelProduct.objects.order_by(
        '-publication_date').filter(is_published=True).filter(
        tags__icontains=search_text) if search_text else [])

    store_profile = ModelStoreProfile.objects.all()
    context = {
        'store_profile': store_profile[0] if store_profile else StoreProfile(),
        'user_profile': None,
        'search_text': search_text,
        'posts': [ProductProfile(x) for x in posts]}

    if request.user.is_authenticated:
        profile = UserProfile(request)
        context['user_profile'] = profile if profile else UserProfile(request)

    return render(request, 'search_tag.html', context)


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
                user=user,
                is_admin=False,
                is_superuser=False)
            profile.save()

            return redirect('login')
