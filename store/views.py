import logging
import string

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from django.utils import timezone

import store.models as models
import store.forms as forms

import store.validation as validation
import store.utils as utils


def buy_request(request, product_id, quantity):
    if not request.user.is_authenticated:
        return redirect('index')

    model_product = models.ModelProduct.objects.get(pk=product_id)

    cart_item = utils.get_cart(request, model_product)
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

    profile = utils.get_user_profile(request)
    cart_list = utils.get_cart_list(request)
    total_price = utils.total_price(cart_list)
    total_price_pprint = utils.total_price_pprint(total_price)
    shipping = utils.total_shipping_price(cart_list)
    shipping_pprint = utils.total_shipping_price_pprint(shipping)

    context = {
        'store_profile': utils.get_store_profile(),
        'user_profile': profile,
        'cart_list': cart_list,
        'favorite_product_id_list': [
            x.product_id for x in utils.get_favorite_list(request)],
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
        cart_item = utils.get_cart(request, model_product)
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
    fav = utils.get_favorite(request, model_product)
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
        cart_item = utils.get_cart(request, model_product)
        cart_item.delete()

    return redirect('cart')


def favorite(request):
    if not request.user.is_authenticated:
        return redirect('index')

    profile = utils.get_user_profile(request)
    context = {
        'store_profile': utils.get_store_profile(),
        'user_profile': profile,
        'cart_list': utils.get_cart_list(request),  # nav
        'favorite_list': utils.get_favorite_list(request)}

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
    fav = utils.get_favorite(request, model_product)
    if fav:
        fav.delete()

    return redirect('favorite')


def index(request):
    products = (
        models.ModelProduct.objects.order_by('-publication_date')
        .filter(is_published=True))
    context = {
        'store_profile': utils.get_store_profile(),
        'user_profile': None,
        'cart_list': utils.get_cart_list(request),  # nav
        'products': [x for x in products],
        'highlight_posts': models.ModelProductHighlight.objects.all()}

    if not request.user.is_authenticated:
        return render(request, 'index_for_visitors.html', context)

    if request.user.is_authenticated:
        profile = utils.get_user_profile(request)
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
        'store_profile': utils.get_store_profile(),
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

    profile = utils.get_user_profile(request)
    if profile.is_admin:
        context = {
            'store_profile': utils.get_store_profile(),
            'user_profile': profile,
            'form': forms.FormProductNew,
            'new_product_status': None}

        if request.method == 'POST':
            new_product = models.ModelProduct.objects.create(
                user=request.user,
                title=request.POST['title'],
                title_for_card=utils.product_title_for_card(
                    request.POST['title']),
                title_for_url=utils.product_title_for_url(
                    request.POST['title']),
                price=float(
                    request.POST['price']),
                price_pprint=utils.product_price_pprint(
                    request.POST['price']),
                price_old=float(
                    request.POST['price']),
                price_old_pprint=utils.product_price_pprint(
                    request.POST['price']),
                price_off=utils.product_price_off(
                    request.POST['price'], request.POST['price']),
                price_off_pprint=utils.product_price_off_pprint(
                    request.POST['price'], request.POST['price']),
                price_off_display=(
                    True if 'price_off_display' in request.POST else False),
                times_split_num=int(
                    request.POST['times_split_num']),
                times_split_interest=int(
                    request.POST['times_split_interest']),
                times_split_unit=utils.product_times_split_unit(
                    request.POST['price'],
                    request.POST['times_split_num'],
                    request.POST['times_split_interest']),
                times_split_pprint=utils.product_times_split_pprint(
                    request.POST['price'],
                    request.POST['times_split_num'],
                    request.POST['times_split_interest']),
                shipping_price=float(
                    request.POST['shipping_price']),
                shipping_price_pprint=utils.product_shipping_price_pprint(
                    request.POST['shipping_price']),
                available_quantity=int(
                    request.POST['available_quantity']),
                available_quantity_display=(
                    True if 'available_quantity_display' in request.POST else
                    False),
                max_quantity_per_sale=utils.product_max_quantity_per_sale(
                    request.POST['available_quantity'],
                    request.POST['max_quantity_per_sale']),
                image_1=request.FILES['image_1'],
                image_2=request.FILES.get('image_2', None),
                image_3=request.FILES.get('image_3', None),
                image_4=request.FILES.get('image_4', None),
                image_5=request.FILES.get('image_5', None),
                summary=request.POST['summary'],
                content=request.POST['content'],
                tags=request.POST['tags'],
                publication_date=timezone.now(),
                is_published=(
                    True if 'is_published' in request.POST else False))

            new_product.save()
            return redirect('manage_products')

        return render(request, 'manage_new.html', context)

    return redirect('index')


def manage_products(request):
    if not request.user.is_authenticated:
        return redirect('index')

    profile = utils.get_user_profile(request)
    if profile.is_admin:
        products = (
            models.ModelProduct.objects.order_by('-publication_date')
            .filter(is_published=True))
        context = {
            'store_profile': utils.get_store_profile(),
            'user_profile': profile,
            'products': products[:4]}

        return render(request, 'manage_products.html', context)

    return redirect('index')


def product(request, product_url_title, product_id):
    logging.info(product_url_title)
    model_product = models.ModelProduct.objects.get(pk=product_id)

    context = {
        'store_profile': utils.get_store_profile(),
        'product': model_product,
        'tags': model_product.tags.split(','),
        'favorite': None,
        'cart': None,
        'cart_list': utils.get_cart_list(request),  # nav
        'user_profile': None}

    if not request.user.is_authenticated:
        return render(request, 'product_for_visitors.html', context)

    if request.user.is_authenticated:
        profile = utils.get_user_profile(request)
        context['user_profile'] = profile

        context['favorite'] = utils.get_favorite(request, model_product)
        context['cart'] = utils.get_cart(request, model_product)

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

        cart_item = utils.get_cart(request, model_product)
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

    fav = utils.get_favorite(request, model_product)
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
        'store_profile': utils.get_store_profile(),
        'user_profile': None,
        'cart_list': utils.get_cart_list(request),  # nav
        'search_text': search_text,
        'products': [x for x in products]}

    if request.user.is_authenticated:
        context['user_profile'] = utils.get_user_profile(request)

    return render(request, 'search.html', context)


def search_tag(request):
    search_text = request.GET['q']
    products = (models.ModelProduct.objects.order_by(
        '-publication_date').filter(is_published=True).filter(
        tags__icontains=search_text) if search_text else [])

    context = {
        'store_profile': utils.get_store_profile(),
        'user_profile': None,
        'cart_list': utils.get_cart_list(request),  # nav
        'search_text': search_text,
        'products': [x for x in products]}

    if request.user.is_authenticated:
        context['user_profile'] = utils.get_user_profile(request)

    return render(request, 'search_tag.html', context)


def signup(request):
    if request.user.is_authenticated:
        return redirect('index')

    context = {
        'store_profile': utils.get_store_profile(),
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
