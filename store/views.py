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


def buy(request, product_id):
    if not request.user.is_authenticated:
        return redirect('index')

    model_product = models.ModelProduct.objects.get(pk=product_id)

    cart_item = utils.get_cart(request, model_product)
    if not cart_item:
        new_product = models.ModelProduct.objects.get(pk=product_id)
        cart_item = models.ModelCart.objects.create(
            user=get_object_or_404(User, pk=request.user.id),
            product=new_product,
            times_split_num=1,
            times_split_unit=new_product.price,
            times_split_pprint='1x ' + new_product.price_pprint,
            quantity=1,
            total_price=new_product.price,
            total_price_pprint=new_product.price_pprint)
        cart_item.save()
    return redirect('cart')


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
            'cart_list': utils.get_cart_list(request)}

        return render(request, 'manage_products.html', context)

    return redirect('index')


def manage_products_edit(request, product_url_title, product_id):
    if not request.user.is_authenticated:
        return redirect('index')

    logging.info(product_url_title)
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
            'is_published': post.is_published,
        })
    profile = utils.get_user_profile(request)
    if profile.is_admin:
        context = {
            'store_profile': utils.get_store_profile(),
            'user_profile': profile,
            'form': form,
            'product': post,
            'product_status': None,
            'cart_list': utils.get_cart_list(request)}

        return render(request, 'manage_products_edit.html', context)
    return redirect('manage_products')


def manage_products_edit_save(request, product_id):
    if not request.user.is_authenticated:
        return redirect('index')

    editable = models.ModelProduct.objects.get(pk=product_id)
    if request.method == 'POST':
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
            editable.image_1 = request.FILES['image_1']
        if 'image_2' in request.FILES:
            editable.image_2 = request.FILES['image_2']
        if 'image_3' in request.FILES:
            editable.image_3 = request.FILES['image_3']
        if 'image_4' in request.FILES:
            editable.image_4 = request.FILES['image_4']
        if 'image_5' in request.FILES:
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
        return redirect('manage_products')
    return redirect('manage_products')


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
            'cart_list': utils.get_cart_list(request)}

        return render(request, 'manage_users.html', context)

    return redirect('index')


def manage_users_edit(request, user_username, user_profile_id, status):
    logging.info(user_username)

    if not request.user.is_authenticated:
        return redirect('index')

    profile = utils.get_user_profile(request)
    if not profile.is_admin:
        return redirect('index')

    edit_user_profile = models.ModelUserProfile.objects.get(pk=user_profile_id)
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

    if profile.is_admin:
        context = {
            'store_profile': utils.get_store_profile(),
            'user_profile': profile,
            'edit_user_profile': edit_user_profile,
            'form_user': form_user,
            'form_user_profile': form_user_profile,
            'form_status': None if status == '_' else status,
            'cart_list': utils.get_cart_list(request)}

        return render(request, 'manage_users_edit.html', context)
    return redirect('manage_users')


def manage_users_edit_save(request, edit_user_profile_id):
    if not request.user.is_authenticated:
        return redirect('index')

    profile = utils.get_user_profile(request)
    if not profile.is_admin:
        return redirect('index')

    if request.method == 'POST':
        profile_id = edit_user_profile_id
        edit_user_profile = models.ModelUserProfile.objects.get(pk=profile_id)
        edit_user = get_object_or_404(User, pk=edit_user_profile.user.id)
        status = None

        if 'profile_image' in request.FILES:
            edit_user_profile.profile_image = request.FILES['profile_image']
        edit_user_profile.is_blocked = (
            True if 'is_blocked' in request.POST else False)
        edit_user_profile.save()

        if 'name' in request.POST:
            edit_user.first_name = request.POST['name']

        if 'username' in request.POST:
            username = request.POST['username']
            if not validation.available_username(edit_user, username):
                status = 'O nome de usuário fornecido já está sendo usado'
            else:
                edit_user.username = username

        if not status and 'email' in request.POST:
            email = request.POST['email']
            if not validation.available_email(edit_user, email):
                status = 'O email fornecido já está sendo usado'
            else:
                edit_user.email = email

        password = (
            request.POST['password_confirm']
            if 'password_confirm' in request.POST else None)
        if not status and password:
            pass_err = validation.invalid_password(password, password)
            if pass_err:
                status = pass_err
            else:
                edit_user.set_password(password)

        if status:
            return redirect(
                'manage_users_edit', edit_user.username, profile_id, status)

        edit_user.save()
    return redirect('manage_users')


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
        if 'buy' in request.POST:
            return redirect('buy', product_id)

        cart_item = utils.get_cart(request, model_product)
        if cart_item:
            cart_item.delete()
        else:
            new_product = models.ModelProduct.objects.get(pk=product_id)
            cart_item = models.ModelCart.objects.create(
                user=get_object_or_404(User, pk=request.user.id),
                product=new_product,
                times_split_num=1,
                times_split_unit=new_product.price,
                times_split_pprint='1x ' + new_product.price_pprint,
                quantity=1,
                total_price=new_product.price,
                total_price_pprint=new_product.price_pprint)
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
