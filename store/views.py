import logging
import string

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth

import store.models as models
import store.forms as forms

import store.validation as validation
import store.utils as utilities


def buy_request(request, product_id, quantity):
    if not request.user.is_authenticated:
        return redirect('index')

    model_product = models.ModelProduct.objects.get(pk=product_id)

    cart_item = utilities.get_cart(request, model_product)
    if not cart_item:
        new_product = models.ModelProduct.objects.get(pk=product_id)
        cart_item = models.ModelCart.objects.create(
            user=get_object_or_404(User, pk=request.user.id),
            product=new_product,
            quantity=int(quantity))
        cart_item.save()

    return redirect('cart')


def cart(request):
    if not request.user.is_authenticated:
        return redirect('index')

    profile = utilities.get_user_profile(request)
    cart_list = utilities.get_cart_list(request)
    total_price = utilities.total_price(cart_list)
    total_price_pprint = utilities.total_price_pprint(total_price)
    shipping = utilities.total_shipping_price(cart_list)
    shipping_pprint = utilities.total_shipping_price_pprint(shipping)

    context = {
        'store_profile': utilities.get_store_profile(),
        'user_profile': profile,
        'cart_list': cart_list,
        'favorite_product_id_list': [
            x.product_id for x in utilities.get_favorite_list(request)],
        'cart_url': True,
        'shipping_price': shipping,
        'shipping_price_pprint': shipping_pprint,
        'total_price': total_price,
        'total_price_pprint': total_price_pprint}

    if not profile:
        return redirect('index')

    if profile:
        if profile.is_admin:
            return redirect('index')

        if not profile.is_admin:
            return render(request, 'cart.html', context)


def cart_edit(request, product_id):
    if not request.user.is_authenticated:
        return redirect('index')

    model_product = models.ModelProduct.objects.get(pk=product_id)

    if request.method == 'POST':
        cart_item = utilities.get_cart(request, model_product)
        cart_item.delete()

        quantity = request.POST['quantity']
        new_product = models.ModelProduct.objects.get(pk=product_id)
        cart_item = models.ModelCart.objects.create(
            user=get_object_or_404(User, pk=request.user.id),
            product=new_product,
            quantity=int(quantity))
        cart_item.save()

    return redirect('cart')


def cart_favorite(request, product_id):
    if not request.user.is_authenticated:
        return redirect('index')

    model_product = models.ModelProduct.objects.get(pk=product_id)
    fav = utilities.get_favorite(request, model_product)
    if fav:
        fav.delete()
    else:
        fav = models.ModelFavorite.objects.create(
            user=get_object_or_404(User, pk=request.user.id),
            product=model_product)
        fav.save()

    return redirect('cart')


def cart_remove(request, product_id):
    if not request.user.is_authenticated:
        return redirect('index')

    model_product = models.ModelProduct.objects.get(pk=product_id)

    if request.method == 'POST':
        cart_item = utilities.get_cart(request, model_product)
        cart_item.delete()

    return redirect('cart')


def favorite(request):
    if not request.user.is_authenticated:
        return redirect('index')

    profile = utilities.get_user_profile(request)
    context = {
        'store_profile': utilities.get_store_profile(),
        'user_profile': profile,
        'cart_list': utilities.get_cart_list(request),  # nav
        'favorite_list': utilities.get_favorite_list(request)}

    if not profile:
        return redirect('index')

    if profile:
        if profile.is_admin:
            return redirect('index')

        if not profile.is_admin:
            return render(request, 'favorite.html', context)


def favorite_remove(request, product_id):
    if not request.user.is_authenticated:
        return redirect('index')

    model_product = models.ModelProduct.objects.get(pk=product_id)
    fav = utilities.get_favorite(request, model_product)
    if fav:
        fav.delete()

    return redirect('favorite')


def index(request):
    products = (
        models.ModelProduct.objects.order_by('-publication_date')
        .filter(is_published=True))
    context = {
        'store_profile': utilities.get_store_profile(),
        'user_profile': None,
        'cart_list': utilities.get_cart_list(request),  # nav
        'products': [x for x in products],
        'highlight_posts': models.ModelProductHighlight.objects.all()}

    if not request.user.is_authenticated:
        return render(request, 'index_for_visitors.html', context)

    if request.user.is_authenticated:
        profile = utilities.get_user_profile(request)
        context['user_profile'] = profile

        if not profile:
            return render(request, 'index_for_users.html', context)

        if profile:
            if not profile.is_admin:
                return render(request, 'index_for_users.html', context)
            if profile.is_admin:
                return render(request, 'index_for_admins.html', context)


def login(request):
    context = {
        'store_profile': utilities.get_store_profile(),
        'user_profile': None,
        'form': forms.FormLogin,
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


def manage_products_new(request):
    if not request.user.is_authenticated:
        return redirect('index')

    profile = utilities.get_user_profile(request)
    if profile.is_admin:
        context = {
            'store_profile': utilities.get_store_profile(),
            'user_profile': profile,
            'form': forms.FormProductNew,
            'new_product_status': None}

        return render(request, 'manage_new.html', context)

    return redirect('index')


def manage_products(request):
    if not request.user.is_authenticated:
        return redirect('index')

    profile = utilities.get_user_profile(request)
    if profile.is_admin:
        products = (
            models.ModelProduct.objects.order_by('-publication_date')
            .filter(is_published=True))
        context = {
            'store_profile': utilities.get_store_profile(),
            'user_profile': profile,
            'products': products[:4]}

        return render(request, 'manage_products.html', context)

    return redirect('index')


def product(request, product_url_title, product_id):
    logging.info(product_url_title)
    model_product = models.ModelProduct.objects.get(pk=product_id)

    context = {
        'store_profile': utilities.get_store_profile(),
        'product': model_product,
        'tags': model_product.tags.split(','),
        'favorite': None,
        'cart': None,
        'cart_list': utilities.get_cart_list(request),  # nav
        'user_profile': None}

    if not request.user.is_authenticated:
        return render(request, 'product_for_visitors.html', context)

    if request.user.is_authenticated:
        profile = utilities.get_user_profile(request)
        context['user_profile'] = profile

        context['favorite'] = utilities.get_favorite(request, model_product)
        context['cart'] = utilities.get_cart(request, model_product)

        if not profile.is_admin and not profile.is_superuser:
            return render(request, 'product_for_users.html', context)

        if profile.is_admin or profile.is_superuser:
            return render(request, 'product_for_admins.html', context)


def product_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('index')

    model_product = models.ModelProduct.objects.get(pk=product_id)

    if request.method == 'POST':
        quantity = request.POST['quantity']

        if 'buy' in request.POST:
            return redirect('buy_request', product_id, quantity)

        cart_item = utilities.get_cart(request, model_product)
        if cart_item:
            cart_item.delete()
        else:
            new_product = models.ModelProduct.objects.get(pk=product_id)
            cart_item = models.ModelCart.objects.create(
                user=get_object_or_404(User, pk=request.user.id),
                product=new_product,
                quantity=int(quantity))
            cart_item.save()

    return redirect('product', model_product.title_for_url, model_product.id)


def product_favorite(request, product_id):
    if not request.user.is_authenticated:
        return redirect('index')

    model_product = models.ModelProduct.objects.get(pk=product_id)

    fav = utilities.get_favorite(request, model_product)
    if fav:
        fav.delete()
    else:
        fav = models.ModelFavorite.objects.create(
            user=get_object_or_404(User, pk=request.user.id),
            product=model_product)
        fav.save()

    return redirect('product', model_product.title_for_url, model_product.id)


def search(request):
    search_text = request.GET['q']
    products = (models.ModelProduct.objects.order_by(
        '-publication_date').filter(is_published=True).filter(
        title__icontains=search_text) if search_text else [])

    context = {
        'store_profile': utilities.get_store_profile(),
        'user_profile': None,
        'cart_list': utilities.get_cart_list(request),  # nav
        'search_text': search_text,
        'products': [x for x in products]}

    if request.user.is_authenticated:
        context['user_profile'] = utilities.get_user_profile(request)

    return render(request, 'search.html', context)


def search_tag(request):
    search_text = request.GET['q']
    products = (models.ModelProduct.objects.order_by(
        '-publication_date').filter(is_published=True).filter(
        tags__icontains=search_text) if search_text else [])

    context = {
        'store_profile': utilities.get_store_profile(),
        'user_profile': None,
        'cart_list': utilities.get_cart_list(request),  # nav
        'search_text': search_text,
        'products': [x for x in products]}

    if request.user.is_authenticated:
        context['user_profile'] = utilities.get_user_profile(request)

    return render(request, 'search_tag.html', context)


def signup(request):
    if request.user.is_authenticated:
        return redirect('index')

    context = {
        'store_profile': utilities.get_store_profile(),
        'user_profile': None,
        'form': forms.FormSignup,
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

            profile = models.ModelUserProfile.objects.create(
                user=user,
                is_admin=False,
                is_superuser=False)
            profile.save()

            return redirect('login')
