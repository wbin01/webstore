import logging

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

import store.models as models
import store.modules.validations as mdl_validations


def dashboard_edition_warnings(request) -> str | None:
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


def edition_warnings(request, edit_user) -> str | None:
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


def new(request) -> str:
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

    user_profile = models.ModelUserProfile.objects.create(
        user=user,
        is_admin=False,
        is_superuser=False)
    user_profile.save()

    return 'success'


def profile(request) -> models.ModelUserProfile:
    """..."""
    try:
        return get_object_or_404(
            models.ModelUserProfile, user=request.user.id)
    except Exception as err:
        logging.error(err)
        user_profile = models.ModelUserProfile.objects.create(
            user=request.user,
            is_admin=False,
            is_superuser=False)
        user_profile.save()
        return get_object_or_404(
            models.ModelUserProfile, user=request.user.id)


def save_dashboard_edition(request, user_profile) -> None:
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
        user_profile.profile_image = None
    else:
        if 'profile_image' in request.FILES:
            user_profile.profile_image = request.FILES['profile_image']

    user_profile.save()


def save_edition(request, edit_user, edit_user_profile) -> None:
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
