import logging
import string

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from django.utils import timezone

import users.models as user_models
import store.models as models
import store.forms as forms

import store.validation as validation
import store.utils as utils


def cart(request):
    if not request.user.is_authenticated:
        return redirect('index')

    profile = utils.get_user_profile(request)
    cart_list = utils.get_cart_list(request)
    shipping = utils.total_shipping_price(cart_list)
    shipping_pprint = utils.total_shipping_price_pprint(shipping)
    total_price = utils.cart_total_price(cart_list)
    total_price_pprint = utils.cart_total_price_pprint(total_price)
    total_price_split_list = utils.cart_total_price_split_list(cart_list)
    total_price_split_list_pprint = utils.cart_total_price_split_list_pprint(
        total_price_split_list)

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
        'total_price_pprint': total_price_pprint,
        'total_price_split_list': total_price_split_list,
        'len_total_price_split_list': len(total_price_split_list),
        'total_price_split_list_pprint': total_price_split_list_pprint}

    if not profile:
        return redirect('index')

    if profile:
        # if profile.is_admin:
        #     return redirect('index')
        # if not profile.is_admin:
        #     return render(request, 'cart.html', context)
        return render(request, 'cart.html', context)


def cart_edit(request, cart_id):
    if not request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        cart_item = models.ModelCart.objects.get(pk=cart_id)
        cart_product = models.ModelProduct.objects.get(pk=cart_item.product.id)

        quantity = int(request.POST['quantity'])
        cart_item.quantity = quantity

        times_split_num = int(request.POST['times_split_num'])
        cart_item.times_split_num = times_split_num

        times_split_unit = utils.cart_edit_times_split_unit(
            cart_product.price,
            quantity,
            times_split_num,
            cart_product.times_split_interest)
        cart_item.times_split_unit = times_split_unit

        cart_item.times_split_pprint = utils.cart_edit_times_split_pprint(
            times_split_num,
            times_split_unit)

        total_price = utils.cart_edit_total_price(
            cart_product.price,
            quantity,
            cart_product.times_split_interest,
            times_split_num)
        cart_item.total_price = total_price

        cart_item.total_price_pprint = utils.cart_edit_total_price_pprint(
            total_price)

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


def manage_products(request):
    if not request.user.is_authenticated:
        return redirect('index')

    profile = utils.get_user_profile(request)

    if profile.is_admin:
        search_text = '' if 'q' not in request.GET else request.GET['q']
        if search_text:
            products = (models.ModelProduct.objects.order_by(
                '-publication_date').filter(
                title__icontains=request.GET['q']) if request.GET['q'] else [])
        else:
            products = (
                models.ModelProduct.objects.order_by('-publication_date'))

        context = {
            'store_profile': utils.get_store_profile(),
            'user_profile': profile,
            'products': products,
            'search_text': search_text,
            'cart_list': utils.get_cart_list(request),
            'manage_url': True}

        return render(request, 'manage_products.html', context)

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
            'new_product_status': None,
            'cart_list': utils.get_cart_list(request)}

        if request.method == 'POST':
            status = validation.invalid_image(request.FILES['image_1'])
            if status:
                context['new_product_status'] = status
                return render(request, 'manage_products_new.html', context)

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

        return render(request, 'manage_products_new.html', context)

    return redirect('index')


def manage_products_edit(request, product_url_title, product_id):
    logging.info(product_url_title)
    if not request.user.is_authenticated:
        return redirect('index')

    profile = utils.get_user_profile(request)
    if not profile.is_admin:
        return redirect('index')

    post = models.ModelProduct.objects.get(pk=product_id)
    form = forms.FormProductNew(
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
            'image_1': post.image_1,
            'image_2': post.image_2,
            'image_3': post.image_3,
            'image_4': post.image_4,
            'image_5': post.image_5,
            'summary': post.summary,
            'content': post.content,
            'tags': post.tags,
            'is_published': post.is_published})
    context = {
        'store_profile': utils.get_store_profile(),
        'user_profile': profile,
        'form': form,
        'product': post,
        'warning': None,
        'cart_list': utils.get_cart_list(request)}

    if request.method != 'POST':
        return render(request, 'manage_products_edit.html', context)

    context['warning'] = __manage_products_get_warning(request)
    if context['warning']:
        return render(request, 'manage_products_edit.html', context)
    __manage_products_edit_save(request, product_id)
    return redirect('manage_products')


def __manage_products_get_warning(request) -> str | None:
    warning = None
    for image in ['image_1', 'image_2', 'image_3', 'image_4', 'image_5']:
        if image in request.FILES:
            warning = validation.invalid_image(request.FILES[image])
            if warning:
                break
    return warning


def __manage_products_edit_save(request, product_id) -> None:
    editable = models.ModelProduct.objects.get(pk=product_id)
    if 'title' in request.POST:
        editable.title = request.POST['title']
        editable.title_for_card = utils.product_title_for_card(
            request.POST['title'])
    if 'price' in request.POST:
        editable.price_old = editable.price
        editable.price_old_pprint = utils.product_price_pprint(
            str(editable.price))
        editable.price = float(request.POST['price'])
        editable.price_pprint = utils.product_price_pprint(
            request.POST['price'])
        editable.price_off = utils.product_price_off(
            request.POST['price'], str(editable.price_old))
        editable.price_off_pprint = utils.product_price_off_pprint(
            request.POST['price'], str(editable.price_old))
    if 'times_split_num' in request.POST:
        editable.times_split_num = int(request.POST['times_split_num'])
    if 'times_split_interest' in request.POST:
        editable.times_split_interest = int(
            request.POST['times_split_interest'])
    if 'shipping_price' in request.POST:
        editable.shipping_price = float(request.POST['shipping_price'])
        editable.shipping_price_pprint = (
            utils.product_shipping_price_pprint(
                request.POST['shipping_price']))
    if 'available_quantity' in request.POST:
        editable.available_quantity = int(
            request.POST['available_quantity'])
    if 'max_quantity_per_sale' in request.POST:
        editable.max_quantity_per_sale = (
            utils.product_max_quantity_per_sale(
                request.POST['available_quantity'],
                request.POST['max_quantity_per_sale']))
    if 'image_1' in request.FILES:
        if not validation.invalid_image(request.FILES['image_1']):
            editable.image_1 = request.FILES['image_1']
    if 'image_2' in request.FILES:
        if not validation.invalid_image(request.FILES['image_2']):
            editable.image_2 = request.FILES['image_2']
    if 'image_3' in request.FILES:
        if not validation.invalid_image(request.FILES['image_3']):
            editable.image_3 = request.FILES['image_3']
    if 'image_4' in request.FILES:
        if not validation.invalid_image(request.FILES['image_4']):
            editable.image_4 = request.FILES['image_4']
    if 'image_5' in request.FILES:
        if not validation.invalid_image(request.FILES['image_5']):
            editable.image_5 = request.FILES['image_5']
    if 'summary' in request.POST:
        editable.summary = request.POST['summary']
    if 'content' in request.POST:
        editable.content = request.POST['content']
    if 'tags' in request.POST:
        editable.tags = request.POST['tags']
    if ('price' not in request.POST or
            'times_split_num' not in request.POST or
            'times_split_interest' not in request.POST):
        context['product_status'] = 'há campos vazios'
    else:
        editable.times_split_unit = utils.product_times_split_unit(
            request.POST['price'],
            request.POST['times_split_num'],
            request.POST['times_split_interest'])
        editable.times_split_pprint = utils.product_times_split_pprint(
            request.POST['price'],
            request.POST['times_split_num'],
            request.POST['times_split_interest'])
    editable.publication_date = timezone.now()
    editable.price_off_display = (
        True if 'price_off_display' in request.POST else False)
    editable.available_quantity_display = (
        True if 'available_quantity_display' in request.POST else
        False)
    editable.is_published = (
        True if 'is_published' in request.POST else False)

    editable.save()


def manage_store(request):
    if not request.user.is_authenticated:
        return redirect('index')

    profile = utils.get_user_profile(request)
    if not profile.is_admin:
        return redirect('index')

    store_profile = utils.get_store_profile()
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
        'cart_list': utils.get_cart_list(request),
        'manage_url': True,
        'form': form_store_profile}

    """
    context['warning'] = __manage_products_get_warning(request)
    if context['warning']:
        return render(request, 'manage_products_edit.html', context)
    __manage_products_edit_save(request, product_id)
    return redirect('manage_products')
    """
    if request.method != 'POST':
        return render(request, 'manage_store.html', context)

    context['warning'] = __manage_store_get_warning(request)
    if context['warning']:
        return render(request, 'manage_store.html', context)
    __manage_store_save(request, store_profile)
    return redirect('manage_store')


def __manage_store_get_warning(request) -> str | None:
    warning = None
    if 'brand_image' in request.FILES:
        warning = validation.invalid_image(request.FILES['brand_image'])
    return warning


def __manage_store_save(request, store_profile):
    if 'brand_name' in request.POST:
        store_profile.brand_name = request.POST['brand_name']
    store_profile.show_brand_name_on_nav = (
        True if 'show_brand_name_on_nav' in request.POST else False)

    if 'brand_image' in request.FILES:
        store_profile.brand_image = request.FILES['brand_image']
    store_profile.show_brand_image_on_nav = (
        True if 'show_brand_image_on_nav' in request.POST else False)

    if 'theme_color' in request.POST:
        store_profile.theme_color = request.POST['theme_color']

    if 'theme_color_text' in request.POST:
        store_profile.theme_color_text = request.POST['theme_color_text']

    if 'social_media_facebook' in request.POST:
        store_profile.social_media_facebook = (
            request.POST['social_media_facebook'])
    if 'social_media_whatsapp' in request.POST:
        store_profile.social_media_whatsapp = (
            request.POST['social_media_whatsapp'])
    if 'social_media_twitter' in request.POST:
        store_profile.social_media_twitter = (
            request.POST['social_media_twitter'])
    if 'social_media_youtube' in request.POST:
        store_profile.social_media_youtube = (
            request.POST['social_media_youtube'])
    if 'social_media_instagram' in request.POST:
        store_profile.social_media_instagram = (
            request.POST['social_media_instagram'])
    if 'social_media_twitch' in request.POST:
        store_profile.social_media_twitch = (
            request.POST['social_media_twitch'])
    if 'social_media_discord' in request.POST:
        store_profile.social_media_discord = (
            request.POST['social_media_discord'])
    if 'social_media_linkedin' in request.POST:
        store_profile.social_media_linkedin = (
            request.POST['social_media_linkedin'])
    if 'social_media_github' in request.POST:
        store_profile.social_media_github = (
            request.POST['social_media_github'])
    if 'social_media_other' in request.POST:
        store_profile.social_media_other = (
            request.POST['social_media_other'])
    store_profile.save()


def manage_users(request):
    if not request.user.is_authenticated:
        return redirect('index')

    profile = utils.get_user_profile(request)
    if profile.is_admin:
        search_text = '' if 'q' not in request.GET else request.GET['q']
        if search_text:
            user_profiles = (
                models.ModelUserProfile.objects.filter(
                    user__first_name__icontains=search_text)
                if search_text else [])
        else:
            user_profiles = models.ModelUserProfile.objects.all()

        context = {
            'store_profile': utils.get_store_profile(),
            'user_profile': profile,
            'users': user_profiles,
            'search_text': '',
            'status': '_',
            'cart_list': utils.get_cart_list(request),
            'manage_url': True}

        return render(request, 'manage_users.html', context)

    return redirect('index')


def manage_users_edit(request, user_username, user_profile_id):
    logging.info(user_username)
    if not request.user.is_authenticated:
        return redirect('index')

    profile = utils.get_user_profile(request)
    if not profile.is_admin:
        return redirect('index')

    edit_user_profile = models.ModelUserProfile.objects.get(pk=user_profile_id)
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
        'store_profile': utils.get_store_profile(),
        'user_profile': profile,
        'edit_user_profile': edit_user_profile,
        'form_user': form_user,
        'form_user_profile': form_user_profile,
        'warning': None,
        'cart_list': utils.get_cart_list(request)}

    if request.method != 'POST':
        return render(request, 'manage_users_edit.html', context)

    context['warning'] = __manage_users_get_warning(request, edit_user)
    if context['warning']:
        return render(request, 'manage_users_edit.html', context)
    __manage_users_edit_save(request, edit_user, edit_user_profile)
    return redirect('manage_users')


def __manage_users_get_warning(request, edit_user) -> str | None:
    warning = None
    if 'profile_image' in request.FILES:
        warning = validation.invalid_image(request.FILES['profile_image'])

    if 'username' in request.POST:
        username = request.POST['username']
        if not validation.available_username(edit_user, username):
            warning = 'O nome de usuário fornecido já está sendo usado'

    if 'email' in request.POST:
        if not validation.available_email(edit_user, request.POST['email']):
            warning = 'O email fornecido já está sendo usado'

    if 'password_confirm' in request.POST:
        password = request.POST['password_confirm']
        password = None if not password else password
        if password:
            warning = validation.invalid_password(password, password)

    return warning


def __manage_users_edit_save(request, edit_user, edit_user_profile) -> None:
    if 'name' in request.POST:
        edit_user.first_name = request.POST['name']
    if 'username' in request.POST:
        edit_user.username = request.POST['username']
    if 'email' in request.POST:
        edit_user.email = request.POST['email']
    if 'password_confirm' in request.POST:
        password = request.POST['password_confirm']
        password = None if not password else password
        edit_user.set_password(password)
    edit_user.save()

    if 'profile_image' in request.FILES:
        edit_user_profile.profile_image = request.FILES['profile_image']
    edit_user_profile.is_blocked = (
        True if 'is_blocked' in request.POST else False)
    edit_user_profile.save()


def manage_users_new(request):
    if not request.user.is_authenticated:
        return redirect('index')

    profile = utils.get_user_profile(request)
    if profile.is_admin:
        context = {
            'store_profile': utils.get_store_profile(),
            'user_profile': profile,
            'form': forms.FormSignup,
            'status': None,
            'cart_list': utils.get_cart_list(request)}

        if request.method != 'POST':
            return render(request, 'manage_users_new.html', context)
        else:
            new_user_status = __create_new_user(request)
            if new_user_status != 'success':
                context['status'] = new_user_status
                return render(request, 'manage_users_new.html', context)
            return redirect('manage_users')

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

    if request.method == 'POST':
        cart_item = utils.get_cart(request, model_product)
        if 'buy' in request.POST:
            if not cart_item:
                __create_cart_item(request.user.id, model_product)
            return redirect('cart')

        if 'add_favorite' in request.POST:
            __create_favorite_item(request.user.id, model_product)
        elif 'remove_favorite' in request.POST:
            fav_item = utils.get_favorite(request, model_product)
            fav_item.delete()

        elif 'add_cart' in request.POST:
            __create_cart_item(request.user.id, model_product)
        elif 'remove_cart' in request.POST:
            cart_item.delete()

    profile = utils.get_user_profile(request)
    context['user_profile'] = profile
    context['favorite'] = utils.get_favorite(request, model_product)
    context['cart'] = utils.get_cart(request, model_product)

    if not profile.is_admin and not profile.is_superuser:
        return render(request, 'product_for_users.html', context)
    if profile.is_admin or profile.is_superuser:
        return render(request, 'product_for_admins.html', context)


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
        else:
            new_user_status = __create_new_user(request)
            if new_user_status != 'success':
                context['signup_status'] = new_user_status
                return render(request, 'signup.html', context)
            return redirect('login')


def user_dashboard(request, username, status):
    logging.info(username)

    if not request.user.is_authenticated:
        return redirect('index')

    profile = utils.get_user_profile(request)
    # if profile.is_admin:  # REVISÃO
    #     return redirect('index')
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

    # if profile.is_admin:
    context = {
        'store_profile': utils.get_store_profile(),
        'user_profile': profile,
        'form_user': form_user,
        'form_user_profile': form_user_profile,
        'form_status': None if status == 'dashboard' else status,
        'cart_list': utils.get_cart_list(request)}

    return render(request, 'user_dashboard.html', context)


def __create_new_user(request) -> str:
    """Create new user

    Create a user and their profile

    :param request: request
    :return: "success" str or a message with the error
    """
    name = request.POST['name']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    password_confirm = request.POST['password_confirm']

    space_err = validation.invalid_whitespace(
        [name, username, email, password, password_confirm])
    if space_err:
        return space_err

    username_err = validation.invalid_username(username)
    if username_err:
        return username_err

    email_err = validation.invalid_email(email)
    if email_err:
        return email_err

    pass_err = validation.invalid_password(password, password_confirm)
    if pass_err:
        return pass_err

    if User.objects.filter(username=email).exists():
        return 'Usuário já cadastrado'

    if User.objects.filter(email=email).exists():
        return 'Email já cadastrado'

    user = User.objects.create_user(
        username=username, first_name=name,
        email=email, password=password)
    user.save()

    profile = models.ModelUserProfile.objects.create(
        user=user,
        is_admin=False,
        is_superuser=False)
    profile.save()

    return 'success'


def __create_cart_item(user_id, model_product) -> None:
    cart_item = models.ModelCart.objects.create(
        user=get_object_or_404(User, pk=user_id),
        product=model_product,
        times_split_num=1,
        times_split_unit=model_product.price,
        times_split_pprint='1x ' + model_product.price_pprint,
        quantity=1,
        total_price=model_product.price,
        total_price_pprint=model_product.price_pprint)
    cart_item.save()


def __create_favorite_item(user_id, model_product) -> None:
    fav = models.ModelFavorite.objects.create(
        user=get_object_or_404(User, pk=user_id),
        product=model_product)
    fav.save()
