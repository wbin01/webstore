import logging
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from django.utils import timezone

import store.models as store_models
import store.forms as forms
import store.modules.cart as mdl_cart
import store.modules.favorites as mdl_favorites
import store.modules.product as mdl_product
import store.modules.store as mdl_store
import store.modules.user as mdl_user
import store.modules.validations as mdl_validations


def cart(request):
    if not request.user.is_authenticated:
        return redirect('index')

    profile = mdl_user.profile(request)
    cart_list = mdl_cart.items_list(request)
    shipping = mdl_cart.total_price_with_shipping(cart_list)
    shipping_pprint = mdl_cart.total_price_with_shipping_pprint(shipping)
    total_price = mdl_cart.total_price(cart_list)
    total_price_pprint = mdl_cart.total_price_pprint(total_price)
    total_price_split_list = mdl_cart.total_price_split_list(cart_list)
    total_price_split_list_pprint = (
        mdl_cart.total_price_split_list_pprint(total_price_split_list))

    context = {
        'store_profile': mdl_store.profile(),
        'user_profile': profile,
        'cart_list': cart_list,
        'favorite_product_id_list': [
            x.product_id for x in mdl_favorites.items_list(request)],
        'cart_url': True,
        'shipping_price': shipping,
        'shipping_price_pprint': shipping_pprint,
        'total_price': total_price,
        'total_price_pprint': total_price_pprint,
        'total_price_split_list': total_price_split_list,
        'len_total_price_split_list': len(total_price_split_list),
        'total_price_split_list_pprint': total_price_split_list_pprint}

    if request.method != 'POST':
        return render(request, 'cart.html', context)

    if 'edit_item' in request.POST:
        mdl_cart.edit_item(request)
    elif 'remove_item' in request.POST:
        mdl_cart.remove_item(request)
    elif 'add_to_favorites' in request.POST:
        mdl_cart.add_to_favorites(request)
    elif 'remove_from_favorites' in request.POST:
        mdl_cart.remove_from_favorites(request)

    return redirect('cart')


def favorite(request):
    if not request.user.is_authenticated:
        return redirect('index')

    profile = mdl_user.profile(request)
    context = {
        'store_profile': mdl_store.profile(),
        'user_profile': profile,
        'cart_list': mdl_cart.items_list(request),  # nav
        'favorite_list': mdl_favorites.items_list(request)}

    if request.method != 'POST':
        return render(request, 'favorite.html', context)

    if 'remove_from_favorites' in request.POST:
        mdl_favorites.remove_item(request)
    return redirect('favorite')


def index(request):
    products = (
        store_models.ModelProduct.objects.order_by('-publication_date')
        .filter(is_published=True))
    context = {
        'store_profile': mdl_store.profile(),
        'user_profile': None,
        'cart_list': mdl_cart.items_list(request),  # nav
        'products': [x for x in products],
        'highlight_posts': store_models.ModelProductHighlight.objects.all()}

    if not request.user.is_authenticated:
        return render(request, 'index_for_visitors.html', context)

    if request.user.is_authenticated:
        profile = mdl_user.profile(request)
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
        'store_profile': mdl_store.profile(),
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


def manage_products(request):
    if not request.user.is_authenticated:
        return redirect('index')

    profile = mdl_user.profile(request)

    if profile.is_admin:
        search_text = '' if 'q' not in request.GET else request.GET['q']
        if search_text:
            products = (store_models.ModelProduct.objects.order_by(
                '-publication_date').filter(
                title__icontains=request.GET['q']) if request.GET['q'] else [])
        else:
            products = store_models.ModelProduct.objects.order_by(
                '-publication_date')

        context = {
            'store_profile': mdl_store.profile(),
            'user_profile': profile,
            'products': products,
            'search_text': search_text,
            'cart_list': mdl_cart.items_list(request),
            'manage_url': True}

        return render(request, 'manage_products.html', context)

    return redirect('index')


def manage_products_new(request):
    if not request.user.is_authenticated:
        return redirect('index')

    profile = mdl_user.profile(request)
    if profile.is_admin:
        context = {
            'store_profile': mdl_store.profile(),
            'user_profile': profile,
            'form': forms.FormProductNew,
            'new_product_status': None,
            'cart_list': mdl_cart.items_list(request)}

        if request.method == 'POST':
            status = mdl_validations.invalid_image(request.FILES['image_1'])
            if status:
                context['new_product_status'] = status
                return render(request, 'manage_products_new.html', context)

            content_text = request.POST['content']
            content_text = (
                json.loads(content_text)['html'] if content_text else '')

            new_product = store_models.ModelProduct.objects.create(
                user=request.user,
                title=request.POST['title'],
                title_for_card=mdl_product.card_title(
                    request.POST['title']),
                title_for_url=mdl_product.url_title(
                    request.POST['title']),
                price=float(
                    request.POST['price']),
                price_pprint=mdl_product.price_pprint(
                    request.POST['price']),
                price_old=float(
                    request.POST['price']),
                price_old_pprint=mdl_product.price_pprint(
                    request.POST['price']),
                price_off=mdl_product.price_off(
                    request.POST['price'], request.POST['price']),
                price_off_pprint=mdl_product.price_off_pprint(
                    request.POST['price'], request.POST['price']),
                price_off_display=(
                    True if 'price_off_display' in request.POST else False),
                times_split_num=int(
                    request.POST['times_split_num']),
                times_split_interest=int(
                    request.POST['times_split_interest']),
                times_split_unit=mdl_product.split_unit(
                    request.POST['price'],
                    request.POST['times_split_num'],
                    request.POST['times_split_interest']),
                times_split_pprint=mdl_product.split_pprint(
                    request.POST['price'],
                    request.POST['times_split_num'],
                    request.POST['times_split_interest']),
                shipping_price=float(
                    request.POST['shipping_price']),
                shipping_price_pprint=(
                    mdl_product.shipping_price_pprint(
                        request.POST['shipping_price'])),
                available_quantity=int(
                    request.POST['available_quantity']),
                available_quantity_display=(
                    True if 'available_quantity_display' in request.POST else
                    False),
                max_quantity_per_sale=(
                    mdl_product.max_quantity_per_sale(
                        request.POST['available_quantity'],
                        request.POST['max_quantity_per_sale'])),
                image_1=request.FILES['image_1'],
                image_2=request.FILES.get('image_2', None),
                image_3=request.FILES.get('image_3', None),
                image_4=request.FILES.get('image_4', None),
                image_5=request.FILES.get('image_5', None),
                content=content_text,
                tags=request.POST['tags'],
                publication_date=timezone.now(),
                is_published=(
                    True if 'is_published' in request.POST else False))

            new_product.save()
            return redirect('manage_products')

        return render(request, 'manage_products_new.html', context)

    return redirect('index')


def manage_products_edit(request, product_url_title, product_id):
    logging.info(product_url_title)
    if not request.user.is_authenticated:
        return redirect('index')

    profile = mdl_user.profile(request)
    if not profile.is_admin:
        return redirect('index')

    post = store_models.ModelProduct.objects.get(pk=product_id)
    form = forms.FormProductEdit(
        initial={
            'title': post.title,
            'price': post.price,
            'price_off_display': post.price_off_display,
            'times_split_num': post.times_split_num,
            'times_split_interest': post.times_split_interest,
            'shipping_price': post.shipping_price,
            'available_quantity': post.available_quantity,
            'available_quantity_display': post.available_quantity_display,
            'max_quantity_per_sale': post.max_quantity_per_sale,
            'content': post.content,
            'tags': post.tags,
            'is_published': post.is_published})
    context = {
        'store_profile': mdl_store.profile(),
        'user_profile': profile,
        'form': form,
        'product': post,
        'warning': None,
        'cart_list': mdl_cart.items_list(request)}

    if request.method != 'POST':
        return render(request, 'manage_products_edit.html', context)

    context['warning'] = mdl_product.edition_warnings(request)
    if context['warning']:
        return render(request, 'manage_products_edit.html', context)
    mdl_product.save_edition(request, product_id)
    return redirect('manage_products')


def manage_store(request):
    if not request.user.is_authenticated:
        return redirect('index')

    profile = mdl_user.profile(request)
    if not profile.is_admin:
        return redirect('index')

    store_profile = mdl_store.profile()
    form_store_profile = forms.FormStoreProfile(
        initial={
            'brand_name': store_profile.brand_name,
            'show_brand_name_on_nav': store_profile.show_brand_name_on_nav,
            # 'brand_image': store_profile.brand_image,
            'show_brand_image_on_nav': (
                store_profile.show_brand_image_on_nav),
            'theme_color': store_profile.theme_color,
            'theme_color_text': store_profile.theme_color_text,
            'social_media_facebook': store_profile.social_media_facebook,
            'social_media_whatsapp': store_profile.social_media_whatsapp,
            'social_media_twitter': store_profile.social_media_twitter,
            'social_media_youtube': store_profile.social_media_youtube,
            'social_media_instagram': store_profile.social_media_instagram,
            'social_media_twitch': store_profile.social_media_twitch,
            'social_media_discord': store_profile.social_media_discord,
            'social_media_linkedin': store_profile.social_media_linkedin,
            'social_media_github': store_profile.social_media_github,
            'social_media_other': store_profile.social_media_other})

    context = {
        'store_profile': store_profile,
        'user_profile': profile,
        'warning': None,
        'cart_list': mdl_cart.items_list(request),
        'manage_url': True,
        'form': form_store_profile}

    if request.method != 'POST':
        return render(request, 'manage_store.html', context)

    context['warning'] = mdl_store.edition_warnings(request)
    if context['warning']:
        return render(request, 'manage_store.html', context)
    mdl_store.save_edition(request, store_profile)
    return redirect('manage_store')


def manage_users(request):
    if not request.user.is_authenticated:
        return redirect('index')

    profile = mdl_user.profile(request)
    if profile.is_admin:
        search_text = '' if 'q' not in request.GET else request.GET['q']
        if search_text:
            user_profiles = (
                store_models.ModelUserProfile.objects.filter(
                    user__first_name__icontains=search_text)
                if search_text else [])
        else:
            user_profiles = store_models.ModelUserProfile.objects.all()

        context = {
            'store_profile': mdl_store.profile(),
            'user_profile': profile,
            'users': user_profiles,
            'search_text': '',
            'status': '_',
            'cart_list': mdl_cart.items_list(request),
            'manage_url': True}

        return render(request, 'manage_users.html', context)

    return redirect('index')


def manage_users_edit(request, user_username, user_profile_id):
    logging.info(user_username)
    if not request.user.is_authenticated:
        return redirect('index')

    profile = mdl_user.profile(request)
    if not profile.is_admin:
        return redirect('index')

    edit_user_profile = store_models.ModelUserProfile.objects.get(
        pk=user_profile_id)
    edit_user = get_object_or_404(User, pk=edit_user_profile.user.id)
    form_user = forms.FormUserEdit(
        initial={
            'name': edit_user_profile.user.first_name,
            'username': edit_user_profile.user.username,
            'email': edit_user_profile.user.email,
        })
    form_user_profile = forms.FormUserProfileEdit(
        initial={
            # 'profile_image': edit_user_profile.profile_image,
            'is_blocked': edit_user_profile.is_blocked,
        }
    )
    context = {
        'store_profile': mdl_store.profile(),
        'user_profile': profile,
        'edit_user_profile': edit_user_profile,
        'form_user': form_user,
        'form_user_profile': form_user_profile,
        'warning': None,
        'cart_list': mdl_cart.items_list(request)}

    if request.method != 'POST':
        return render(request, 'manage_users_edit.html', context)

    context['warning'] = mdl_user.edition_warnings(request, edit_user)
    if context['warning']:
        return render(request, 'manage_users_edit.html', context)
    mdl_user.save_edition(request, edit_user, edit_user_profile)
    return redirect('manage_users')


def manage_users_new(request):
    if not request.user.is_authenticated:
        return redirect('index')

    profile = mdl_user.profile(request)
    if profile.is_admin:
        context = {
            'store_profile': mdl_store.profile(),
            'user_profile': profile,
            'form': forms.FormSignup,
            'status': None,
            'cart_list': mdl_cart.items_list(request)}

        if request.method != 'POST':
            return render(request, 'manage_users_new.html', context)
        else:
            new_user_status = mdl_user.new(request)
            if new_user_status != 'success':
                context['status'] = new_user_status
                return render(request, 'manage_users_new.html', context)
            return redirect('manage_users')

    return redirect('index')


def product(request, product_url_title, product_id):
    logging.info(product_url_title)

    model_product = store_models.ModelProduct.objects.get(pk=product_id)
    context = {
        'store_profile': mdl_store.profile(),
        'product': model_product,
        'tags': model_product.tags.split(','),
        'favorite': None,
        'cart': None,
        'cart_list': mdl_cart.items_list(request),  # nav
        'user_profile': None}

    if not request.user.is_authenticated:
        return render(request, 'product_for_visitors.html', context)

    if request.method == 'POST':
        cart_item = mdl_cart.item(request, model_product)
        if 'buy' in request.POST:
            if not cart_item:
                mdl_cart.new_item(request.user.id, model_product)
            return redirect('cart')

        if 'add_favorite' in request.POST:
            mdl_favorites.new_item(request.user.id, model_product)
        elif 'remove_favorite' in request.POST:
            fav_item = mdl_favorites.item(request, model_product)
            fav_item.delete()

        elif 'add_cart' in request.POST:
            mdl_cart.new_item(request.user.id, model_product)
        elif 'remove_cart' in request.POST:
            cart_item.delete()

    profile = mdl_user.profile(request)
    context['user_profile'] = profile
    context['favorite'] = mdl_favorites.item(request, model_product)
    context['cart'] = mdl_cart.item(request, model_product)

    if not profile.is_admin and not profile.is_superuser:
        return render(request, 'product_for_users.html', context)
    if profile.is_admin or profile.is_superuser:
        return render(request, 'product_for_admins.html', context)


def search(request):
    search_text = request.GET['q']
    products = (store_models.ModelProduct.objects.order_by(
        '-publication_date').filter(is_published=True).filter(
        title__icontains=search_text) if search_text else [])

    context = {
        'store_profile': mdl_store.profile(),
        'user_profile': None,
        'cart_list': mdl_cart.items_list(request),  # nav
        'search_text': search_text,
        'products': [x for x in products]}

    if request.user.is_authenticated:
        context['user_profile'] = mdl_user.profile(request)

    return render(request, 'search.html', context)


def search_tag(request):
    search_text = request.GET['q']
    products = (store_models.ModelProduct.objects.order_by(
        '-publication_date').filter(is_published=True).filter(
        tags__icontains=search_text) if search_text else [])

    context = {
        'store_profile': mdl_store.profile(),
        'user_profile': None,
        'cart_list': mdl_cart.items_list(request),  # nav
        'search_text': search_text,
        'products': [x for x in products]}

    if request.user.is_authenticated:
        context['user_profile'] = mdl_user.profile(request)

    return render(request, 'search_tag.html', context)


def signup(request):
    if request.user.is_authenticated:
        return redirect('index')

    context = {
        'store_profile': mdl_store.profile(),
        'user_profile': None,
        'form': forms.FormSignup,
        'signup_status': None}

    if not request.user.is_authenticated:
        if request.method != 'POST':
            return render(request, 'signup.html', context)
        else:
            new_user_status = mdl_user.new(request)
            if new_user_status != 'success':
                context['signup_status'] = new_user_status
                return render(request, 'signup.html', context)
            return redirect('login')


def user_dashboard(request, username):
    logging.info(username)
    if not request.user.is_authenticated:
        return redirect('index')
    if request.user.username != username:
        return redirect('index')

    profile = mdl_user.profile(request)
    if profile.is_admin:
        return redirect('index')

    form_user = forms.FormUserDashboard(
        initial={
            'name': profile.user.first_name,
            'username': profile.user.username,
            'email': profile.user.email,
            'password': None,
            'password_confirm': None})
    form_user_profile = forms.FormUserDashboardProfile(
        initial={
            # 'profile_image': profile.profile_image,
            'is_blocked': profile.is_blocked})
    context = {
        'store_profile': mdl_store.profile(),
        'user_profile': profile,
        'form_user': form_user,
        'form_user_profile': form_user_profile,
        'warning': None,
        'cart_list': mdl_cart.items_list(request)}

    if request.method != 'POST':
        return render(request, 'user_dashboard.html', context)

    context['warning'] = mdl_user.dashboard_edition_warnings(request)
    if context['warning']:
        return render(request, 'user_dashboard.html', context)

    mdl_user.save_dashboard_edition(request, profile)
    return redirect('user_dashboard', request.user.username)
