import logging

import store.models as models
import store.modules.validations as mdl_validations


def edition_warnings(request) -> str | None:
    # HEX Color
    warning = None
    if 'brand_image' in request.FILES:
        warning = mdl_validations.invalid_image(request.FILES['brand_image'])
    return warning


def profile() -> models.ModelStoreProfile:
    """..."""
    try:
        store_profile = models.ModelStoreProfile.objects.all()
    except Exception as err:
        logging.error(err)
        store_profile = None

    if not store_profile:
        store_profile = models.ModelStoreProfile.objects.create(
            brand_name='Brand',
            show_brand_name_on_nav=True,
            brand_image=None,
            show_brand_image_on_nav=True,
            background_color='#ECECEC',
            theme_color='#8A42AA',
            theme_color_admin='#8F222D',
            theme_color_text='#FFFFFF',
            social_media_facebook=None,
            social_media_whatsapp=None,
            social_media_twitter=None,
            social_media_youtube=None,
            social_media_instagram=None,
            social_media_twitch=None,
            social_media_discord=None,
            social_media_linkedin=None,
            social_media_github=None,
            social_media_other=None)
        store_profile.save()

    store_profile = models.ModelStoreProfile.objects.all()
    return store_profile[0]


def save_edition(request, store_profile):
    if 'brand_name' in request.POST:
        store_profile.brand_name = request.POST['brand_name']
    store_profile.show_brand_name_on_nav = (
        True if 'show_brand_name_on_nav' in request.POST else False)

    remove_image = True if 'remove_brand_image' in request.POST else False
    if remove_image:
        store_profile.brand_image = None
    else:
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
