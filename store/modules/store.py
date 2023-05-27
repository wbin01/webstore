import logging

import store.models as models


def get_store_profile() -> models.ModelStoreProfile:
    """..."""
    try:
        profile = models.ModelStoreProfile.objects.all()
    except Exception as err:
        logging.error(err)
        profile = None

    if not profile:
        profile = models.ModelStoreProfile.objects.create(
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
        profile.save()

    profile = models.ModelStoreProfile.objects.all()
    return profile[0]
