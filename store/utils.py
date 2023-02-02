import string
import logging
from django.shortcuts import get_object_or_404

from store.models import *
import store.models as models


class FullProduct(object):
    """..."""
    def __init__(self, post: models.ModelProduct) -> None:
        """..."""
        self.post = post
        self.id = self.post.id
        self.user = self.post.user
        self.title = self.post.title
        self.url_title = self.__formatted_url_title()
        self.card_title = self.__formatted_card_title()
        self.old_price = self.__formatted_old_price()
        self.new_price = self.__formatted_new_price()
        self.off_price = self.__formatted_off_price()
        self.show_off_price = self.post.show_off_price
        self.times_split_num = self.post.times_split_num
        self.times_split_interest = self.post.times_split_interest
        self.times_split_value = self.__formatted_times_split_value()
        self.times_split_prices = self.__formatted_times_split_prices()
        self.shipping_price = self.__formatted_shipping_price()
        self.image_1 = self.post.image_1
        self.image_2 = self.post.image_2
        self.image_3 = self.post.image_3
        self.image_4 = self.post.image_4
        self.image_5 = self.post.image_5
        self.summary = self.post.summary
        self.content = self.post.content
        self.tags = self.__formatted_tags()
        self.publication_date = self.post.publication_date
        self.is_published = self.post.is_published

    def __formatted_url_title(self) -> str:
        title = ''
        for char in self.post.title:
            char = char.lower()
            if char == ' ' or char in string.ascii_lowercase:
                title += char.replace(' ', '-')
        return title.replace('--', '-')

    def __formatted_card_title(self) -> str:
        """Product name"""
        if len(self.post.title) > 50:
            return self.post.title[:50] + '...'
        return self.post.title

    def __formatted_old_price(self) -> str:
        """R$ 0,00"""

        reais, cents = str(self.post.old_price).split('.')
        if len(cents) == 1:
            cents = f'{cents}0'

        return f'R$ {reais},{cents}'

    def __formatted_new_price(self) -> str:
        """R$ 0,00"""

        reais, cents = str(self.post.new_price).split('.')
        if len(cents) == 1:
            cents = f'{cents}0'

        return f'R$ {reais},{cents}'

    def __formatted_off_price(self) -> str | None:
        """10% OFF"""
        off = 0
        if self.post.old_price > self.post.new_price:
            delta_1 = self.post.old_price - self.post.new_price
            delta_2 = self.post.old_price / 100
            off = round(delta_1 / delta_2)

        if off > 4:
            return f'{off}% OFF'
        return None

    def __formatted_times_split_value(self) -> float | None:
        """5.00

        One unit extracted. If it is 10 times of 5.0, then it returns 5.0
        """
        if self.post.new_price:
            if self.post.times_split_num and self.post.times_split_num > 1:
                preco = self.post.new_price
                vezes = self.post.times_split_num
                juros = self.post.times_split_interest

                preco_real_com_juros = (preco / 100) * juros + preco
                preco = round((preco_real_com_juros / vezes), 2)

                return preco

        return None

    def __formatted_times_split_prices(self) -> str | None:
        """1x R$ 0,00"""
        if self.post.new_price:
            if self.post.times_split_num and self.post.times_split_num > 1:
                preco = self.__formatted_times_split_value()
                reais, centavos = str(preco).split('.')

                if len(centavos) == 1:
                    centavos = f'{centavos}0'

                return '{}x R$ {},{}'.format(
                    self.post.times_split_num, reais, centavos)

        return None

    def __formatted_shipping_price(self) -> str | None:
        """Frete grátis"""
        if not self.post.shipping_price:
            return None
        reais, centavos = str(self.post.shipping_price).split('.')
        if len(centavos) == 1:
            centavos = f'{centavos}0'

        return 'R$ {},{}'.format(reais, centavos)

    def __formatted_tags(self) -> list:
        """[tag1, tag2, tag3]"""
        return [x.strip() for x in self.post.tags.split(',')]


class GenericStoreProfile(object):
    def __init__(self) -> None:
        self.owner = None
        self.brand_name = 'Brand'
        self.show_brand_name_on_nav = True
        self.brand_image = None
        self.show_brand_image_on_nav = True
        self.theme_text_color = '#FFFFFF'
        self.theme_background_color = '#8A42AA'
        self.theme_admin_background_color = '#ff5c33'
        self.social_media_facebook = None
        self.social_media_whatsapp = None
        self.social_media_twitter = None
        self.social_media_youtube = None
        self.social_media_instagram = None
        self.social_media_twitch = None
        self.social_media_discord = None
        self.social_media_linkedin = None
        self.social_media_github = None
        self.social_media_other = None


class GenericUserProfile(object):
    def __init__(self, request):
        self.user = request.user
        try:
            profile = get_object_or_404(
                models.ModelUserProfile, user=request.user.id)
        except Exception as err:
            profile = None
            logging.error(err)

        self.profile_image = profile.profile_image if profile else None
        self.is_admin = profile.is_admin if profile else False
        self.is_superuser = profile.is_superuser if profile else False


def get_cart(request, product) -> models.ModelCart | None:
    """..."""
    try:
        return models.ModelCart.objects.filter(user=request.user.id).filter(
            product_id=product.id)
    except Exception as err:
        logging.error(err)
        return None


def get_favorite(request, product) -> models.ModelFavorite | None:
    try:
        return models.ModelFavorite.objects.filter(
            user=request.user.id).filter(product_id=product.id)
    except Exception as err:
        logging.error(err)
        return None


def get_full_product(model: models.ModelProduct) -> FullProduct:
    """..."""
    return FullProduct(model)


def get_store_profile() -> models.ModelUserProfile | GenericStoreProfile:
    """..."""
    try:
        profile = models.ModelStoreProfile.objects.all()
    except Exception as err:
        logging.error(err)
        profile = None

    if profile:
        return profile[0]
    return GenericStoreProfile()


def get_user_profile(request) -> models.ModelUserProfile | GenericUserProfile:
    """..."""
    try:
        return get_object_or_404(
            models.ModelUserProfile, user=request.user.id)
    except Exception as err:
        logging.error(err)
        return GenericUserProfile(request)
