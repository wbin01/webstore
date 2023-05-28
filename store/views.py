import logging
import json
import string

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from django.utils import timezone

import users.models as user_models
import store.models as models
import store.forms as forms
import store.modules.cart as mdl_cart
import store.modules.favorites as mdl_favorites
import store.modules.pprint_values as mdl_pprint_values
import store.modules.product as mdl_product
import store.modules.store as mdl_store
import store.modules.total_price as mdl_total_price
import store.modules.user as mdl_user
import store.modules.validations as mdl_validations


def cart(request):
    if not request.user.is_authenticated:
        return redirect('index')

    profile = mdl_user.get_user_profile(request)
    cart_list = mdl_cart.get_cart_list(request)
    shipping = mdl_total_price.total_shipping_price(cart_list)
    shipping_pprint = mdl_total_price.total_shipping_price_pprint(shipping)
    total_price = mdl_cart.cart_total_price(cart_list)
    total_price_pprint = mdl_cart.cart_total_price_pprint(total_price)
    total_price_split_list = mdl_cart.cart_total_price_split_list(cart_list)
    total_price_split_list_pprint = (
        mdl_cart.cart_total_price_split_list_pprint(total_price_split_list))

    context = {
        'store_profile': mdl_store.get_store_profile(),
        'user_profile': profile,
        'cart_list': cart_list,
        'favorite_product_id_list': [
            x.product_id for x in mdl_favorites.get_favorite_list(request)],
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

    profile = mdl_user.get_user_profile(request)
    context = {
        'store_profile': mdl_store.get_store_profile(),
        'user_profile': profile,
        'cart_list': mdl_cart.get_cart_list(request),  # nav
        'favorite_list': mdl_favorites.get_favorite_list(request)}

    if request.method != 'POST':
        return render(request, 'favorite.html', context)

    if 'remove_from_favorites' in request.POST:
        mdl_favorites.remove_from_favorites(request)
    return redirect('favorite')


def index(request):
    products = (
        models.ModelProduct.objects.order_by('-publication_date')
        .filter(is_published=True))
    context = {
        'store_profile': mdl_store.get_store_profile(),
        'user_profile': None,
        'cart_list': mdl_cart.get_cart_list(request),  # nav
        'products': [x for x in products],
        'highlight_posts': models.ModelProductHighlight.objects.all()}

    if not request.user.is_authenticated:
        return render(request, 'index_for_visitors.html', context)

    if request.user.is_authenticated:
        profile = mdl_user.get_user_profile(request)
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
        'store_profile': mdl_store.get_store_profile(),
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

    profile = mdl_user.get_user_profile(request)

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
            'store_profile': mdl_store.get_store_profile(),
            'user_profile': profile,
            'products': products,
            'search_text': search_text,
            'cart_list': mdl_cart.get_cart_list(request),
            'manage_url': True}

        return render(request, 'manage_products.html', context)

    return redirect('index')


def manage_products_new(request):
    if not request.user.is_authenticated:
        return redirect('index')

    profile = mdl_user.get_user_profile(request)
    if profile.is_admin:
        context = {
            'store_profile': mdl_store.get_store_profile(),
            'user_profile': profile,
            'form': forms.FormProductNew,
            'new_product_status': None,
            'cart_list': mdl_cart.get_cart_list(request)}

        if request.method == 'POST':
            status = mdl_validations.invalid_image(request.FILES['image_1'])
            if status:
                context['new_product_status'] = status
                return render(request, 'manage_products_new.html', context)

            content_text = request.POST['content']
            content_text = (
                json.loads(content_text)['html'] if content_text else '')

            new_product = models.ModelProduct.objects.create(
                user=request.user,
                title=request.POST['title'],
                title_for_card=mdl_product.product_title_for_card(
                    request.POST['title']),
                title_for_url=mdl_product.product_title_for_url(
                    request.POST['title']),
                price=float(
                    request.POST['price']),
                price_pprint=mdl_product.product_price_pprint(
                    request.POST['price']),
                price_old=float(
                    request.POST['price']),
                price_old_pprint=mdl_product.product_price_pprint(
                    request.POST['price']),
                price_off=mdl_product.product_price_off(
                    request.POST['price'], request.POST['price']),
                price_off_pprint=mdl_product.product_price_off_pprint(
                    request.POST['price'], request.POST['price']),
                price_off_display=(
                    True if 'price_off_display' in request.POST else False),
                times_split_num=int(
                    request.POST['times_split_num']),
                times_split_interest=int(
                    request.POST['times_split_interest']),
                times_split_unit=mdl_product.product_times_split_unit(
                    request.POST['price'],
                    request.POST['times_split_num'],
                    request.POST['times_split_interest']),
                times_split_pprint=mdl_product.product_times_split_pprint(
                    request.POST['price'],
                    request.POST['times_split_num'],
                    request.POST['times_split_interest']),
                shipping_price=float(
                    request.POST['shipping_price']),
                shipping_price_pprint=(
                    mdl_product.product_shipping_price_pprint(
                        request.POST['shipping_price'])),
                available_quantity=int(
                    request.POST['available_quantity']),
                available_quantity_display=(
                    True if 'available_quantity_display' in request.POST else
                    False),
                max_quantity_per_sale=(
                    mdl_product.product_max_quantity_per_sale(
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

    profile = mdl_user.get_user_profile(request)
    if not profile.is_admin:
        return redirect('index')

    post = models.ModelProduct.objects.get(pk=product_id)
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
        'store_profile': mdl_store.get_store_profile(),
        'user_profile': profile,
        'form': form,
        'product': post,
        'warning': None,
        'cart_list': mdl_cart.get_cart_list(request)}

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

    profile = mdl_user.get_user_profile(request)
    if not profile.is_admin:
        return redirect('index')

    store_profile = mdl_store.get_store_profile()
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
        'cart_list': mdl_cart.get_cart_list(request),
        'manage_url': True,
        'form': form_store_profile}

    if request.method != 'POST':
        return render(request, 'manage_store.html', context)

    context['warning'] = mdl_store.edition_warnings(request)
    if context['warning']:
        return render(request, 'manage_store.html', context)
    mdl_store.save_edition(request, store_profile)
    return redirect('manage_store')


# >>>
def manage_users(request):
    if not request.user.is_authenticated:
        return redirect('index')

    profile = mdl_user.get_user_profile(request)
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
            'store_profile': mdl_store.get_store_profile(),
            'user_profile': profile,
            'users': user_profiles,
            'search_text': '',
            'status': '_',
            'cart_list': mdl_cart.get_cart_list(request),
            'manage_url': True}

        return render(request, 'manage_users.html', context)

    return redirect('index')


def manage_users_edit(request, user_username, user_profile_id):
    logging.info(user_username)
    if not request.user.is_authenticated:
        return redirect('index')

    profile = mdl_user.get_user_profile(request)
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
        'store_profile': mdl_store.get_store_profile(),
        'user_profile': profile,
        'edit_user_profile': edit_user_profile,
        'form_user': form_user,
        'form_user_profile': form_user_profile,
        'warning': None,
        'cart_list': mdl_cart.get_cart_list(request)}

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
        warning = mdl_validations.invalid_image(request.FILES['profile_image'])

    if 'username' in request.POST:
        username = request.POST['username']
        if username != edit_user.username:
            if not mdl_validations.available_username(edit_user, username):
                warning = 'O nome de usuário fornecido já está sendo usado'
            if not warning:
                warning = mdl_validations.invalid_username(username)

    if 'email' in request.POST:
        email = request.POST['email']
        if email != edit_user.email:
            if not mdl_validations.available_email(edit_user, email):
                warning = 'O email fornecido já está sendo usado'
            if not warning:
                warning = mdl_validations.invalid_email(email)

    if 'password_confirm' in request.POST:
        password = request.POST['password_confirm']
        password = None if not password else password
        if password:
            warning = mdl_validations.invalid_password(password, password)

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
        if password:
            edit_user.set_password(password)
    edit_user.save()

    remove_image = True if 'remove_image' in request.POST else False
    if remove_image:
        edit_user_profile.profile_image = None
    else:
        if 'profile_image' in request.FILES:
            edit_user_profile.profile_image = request.FILES['profile_image']

    edit_user_profile.is_blocked = (
        True if 'is_blocked' in request.POST else False)
    edit_user_profile.save()


def manage_users_new(request):
    if not request.user.is_authenticated:
        return redirect('index')

    profile = mdl_user.get_user_profile(request)
    if profile.is_admin:
        context = {
            'store_profile': mdl_store.get_store_profile(),
            'user_profile': profile,
            'form': forms.FormSignup,
            'status': None,
            'cart_list': mdl_cart.get_cart_list(request)}

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
        'store_profile': mdl_store.get_store_profile(),
        'product': model_product,
        'tags': model_product.tags.split(','),
        'favorite': None,
        'cart': None,
        'cart_list': mdl_cart.get_cart_list(request),  # nav
        'user_profile': None}

    if not request.user.is_authenticated:
        return render(request, 'product_for_visitors.html', context)

    if request.method == 'POST':
        cart_item = mdl_cart.get_cart(request, model_product)
        if 'buy' in request.POST:
            if not cart_item:
                __create_cart_item(request.user.id, model_product)
            return redirect('cart')

        if 'add_favorite' in request.POST:
            __create_favorite_item(request.user.id, model_product)
        elif 'remove_favorite' in request.POST:
            fav_item = mdl_favorites.get_favorite(request, model_product)
            fav_item.delete()

        elif 'add_cart' in request.POST:
            __create_cart_item(request.user.id, model_product)
        elif 'remove_cart' in request.POST:
            cart_item.delete()

    profile = mdl_user.get_user_profile(request)
    context['user_profile'] = profile
    context['favorite'] = mdl_favorites.get_favorite(request, model_product)
    context['cart'] = mdl_cart.get_cart(request, model_product)

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
        'store_profile': mdl_store.get_store_profile(),
        'user_profile': None,
        'cart_list': mdl_cart.get_cart_list(request),  # nav
        'search_text': search_text,
        'products': [x for x in products]}

    if request.user.is_authenticated:
        context['user_profile'] = mdl_user.get_user_profile(request)

    return render(request, 'search.html', context)


def search_tag(request):
    search_text = request.GET['q']
    products = (models.ModelProduct.objects.order_by(
        '-publication_date').filter(is_published=True).filter(
        tags__icontains=search_text) if search_text else [])

    context = {
        'store_profile': mdl_store.get_store_profile(),
        'user_profile': None,
        'cart_list': mdl_cart.get_cart_list(request),  # nav
        'search_text': search_text,
        'products': [x for x in products]}

    if request.user.is_authenticated:
        context['user_profile'] = mdl_user.get_user_profile(request)

    return render(request, 'search_tag.html', context)


def signup(request):
    if request.user.is_authenticated:
        return redirect('index')

    context = {
        'store_profile': mdl_store.get_store_profile(),
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


def user_dashboard(request, username):
    logging.info(username)
    if not request.user.is_authenticated:
        return redirect('index')
    if request.user.username != username:
        return redirect('index')

    profile = mdl_user.get_user_profile(request)
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
        'store_profile': mdl_store.get_store_profile(),
        'user_profile': profile,
        'form_user': form_user,
        'form_user_profile': form_user_profile,
        'warning': None,
        'cart_list': mdl_cart.get_cart_list(request)}

    if request.method != 'POST':
        return render(request, 'user_dashboard.html', context)

    context['warning'] = __manage_user_dashboard_warning(request)
    if context['warning']:
        return render(request, 'user_dashboard.html', context)

    __manage_user_dashboard_save(request, profile)
    return redirect('user_dashboard', request.user.username)


def __manage_user_dashboard_warning(request) -> str | None:
    warning = None
    if 'profile_image' in request.FILES:
        warning = mdl_validations.invalid_image(request.FILES['profile_image'])

    if 'username' in request.POST:
        username = request.POST['username']
        if username != request.user.username:
            if not mdl_validations.available_username(request.user, username):
                warning = 'O nome de usuário fornecido já está sendo usado'
            if not warning:
                warning = mdl_validations.invalid_username(username)

    if 'email' in request.POST:
        email = request.POST['email']
        if email != request.user.email:
            if not mdl_validations.available_email(request.user, email):
                warning = 'O email fornecido já está sendo usado'
            if not warning:
                warning = mdl_validations.invalid_email(email)

    if 'password' in request.POST and 'password_confirm' in request.POST:
        password = request.POST['password']
        password = None if not password else password

        password_confirm = request.POST['password_confirm']
        password_confirm = None if not password_confirm else password_confirm

        if password and password_confirm:
            warning = mdl_validations.invalid_password(
                password, password_confirm)
        elif password_confirm and not password:
            warning = 'Coloque a senha atual'

    return warning


def __manage_user_dashboard_save(request, profile) -> None:
    if 'name' in request.POST:
        request.user.first_name = request.POST['name']
    if 'username' in request.POST:
        request.user.username = request.POST['username']
    if 'email' in request.POST:
        request.user.email = request.POST['email']
    if 'password' in request.POST and 'password_confirm' in request.POST:
        password = request.POST['password']
        password = None if not password else password
        password_confirm = request.POST['password_confirm']
        password_confirm = None if not password_confirm else password_confirm
        if password and password_confirm:
            request.user.set_password(password)

    request.user.save()

    remove_image = True if 'remove_image' in request.POST else False
    if remove_image:
        profile.profile_image = None
    else:
        if 'profile_image' in request.FILES:
            profile.profile_image = request.FILES['profile_image']

    profile.save()


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

    space_err = mdl_validations.invalid_whitespace(
        [name, username, email, password, password_confirm])
    if space_err:
        return space_err

    username_err = mdl_validations.invalid_username(username)
    if username_err:
        return username_err

    email_err = mdl_validations.invalid_email(email)
    if email_err:
        return email_err

    pass_err = mdl_validations.invalid_password(password, password_confirm)
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
