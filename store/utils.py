import string
import logging
from django.shortcuts import get_object_or_404

import store.models as models


class FullProduct(object):
    """..."""
    def __init__(self, product: models.ModelProduct) -> None:
        """..."""
        self.product = product
        self.id = self.product.id
        self.user = self.product.user
        self.title = self.product.title
        self.url_title = self.__formatted_url_title()
        self.card_title = self.__formatted_card_title()
        self.old_price = self.__formatted_old_price()
        self.new_price = self.__formatted_new_price()
        self.off_price = self.__formatted_off_price()
        self.show_off_price = self.product.show_off_price
        self.times_split_num = self.product.times_split_num
        self.times_split_interest = self.product.times_split_interest
        self.times_split_value = self.__formatted_times_split_value()
        self.times_split_prices = self.__formatted_times_split_prices()
        self.shipping_price = self.__formatted_shipping_price()
        self.available_quantity = self.product.available_quantity
        self.show_available_quantity = self.product.show_available_quantity
        self.max_quantity_per_sale = self.__formatted_max_quantity_per_sale()
        self.image_1 = self.product.image_1
        self.image_2 = self.product.image_2
        self.image_3 = self.product.image_3
        self.image_4 = self.product.image_4
        self.image_5 = self.product.image_5
        self.summary = self.product.summary
        self.content = self.product.content
        self.tags = self.__formatted_tags()
        self.publication_date = self.product.publication_date
        self.is_published = self.product.is_published

    def __formatted_url_title(self) -> str:
        title = ''
        for char in self.product.title:
            char = char.lower()
            if char == ' ' or char in string.ascii_lowercase:
                title += char.replace(' ', '-')
        return title.replace('--', '-')

    def __formatted_card_title(self) -> str:
        """Product name"""
        if len(self.product.title) > 50:
            return self.product.title[:50] + '...'
        return self.product.title

    def __formatted_old_price(self) -> str:
        """R$ 0,00"""

        reais, cents = str(self.product.old_price).split('.')
        if len(cents) == 1:
            cents = f'{cents}0'

        return f'R$ {reais},{cents}'

    def __formatted_new_price(self) -> str:
        """R$ 0,00"""

        reais, cents = str(self.product.new_price).split('.')
        if len(cents) == 1:
            cents = f'{cents}0'

        return f'R$ {reais},{cents}'

    def __formatted_off_price(self) -> str | None:
        """10% OFF"""
        off = 0
        if self.product.old_price > self.product.new_price:
            delta_1 = self.product.old_price - self.product.new_price
            delta_2 = self.product.old_price / 100
            off = round(delta_1 / delta_2)

        if off > 4:
            return f'{off}% OFF'
        return None

    def __formatted_times_split_value(self) -> float | None:
        """5.00

        One unit extracted. If it is 10 times of 5.0, then it returns 5.0
        """
        if self.product.new_price:
            if (self.product.times_split_num and
                    self.product.times_split_num > 1):
                preco = self.product.new_price
                vezes = self.product.times_split_num
                juros = self.product.times_split_interest

                preco_real_com_juros = (preco / 100) * juros + preco
                preco = round((preco_real_com_juros / vezes), 2)

                return preco

        return None

    def __formatted_times_split_prices(self) -> str | None:
        """1x R$ 0,00"""
        if self.product.new_price:
            if (self.product.times_split_num and
                    self.product.times_split_num > 1):
                preco = self.__formatted_times_split_value()
                reais, centavos = str(preco).split('.')

                if len(centavos) == 1:
                    centavos = f'{centavos}0'

                return '{}x R$ {},{}'.format(
                    self.product.times_split_num, reais, centavos)

        return None

    def __formatted_shipping_price(self) -> str | None:
        """Frete grátis"""
        if not self.product.shipping_price:
            return None
        reais, centavos = str(self.product.shipping_price).split('.')
        if len(centavos) == 1:
            centavos = f'{centavos}0'

        return 'R$ {},{}'.format(reais, centavos)

    def __formatted_max_quantity_per_sale(self) -> int:
        if (self.product.available_quantity <
                self.product.max_quantity_per_sale):
            return self.product.available_quantity
        return self.product.max_quantity_per_sale

    def __formatted_tags(self) -> list:
        """[tag1, tag2, tag3]"""
        return [x.strip() for x in self.product.tags.split(',')]


class GenericStoreProfile(object):
    def __init__(self) -> None:
        self.owner = None
        self.brand_name = 'Brand'
        self.show_brand_name_on_nav = True
        self.brand_image = None
        self.show_brand_image_on_nav = True
        self.theme_text_color = '#FFFFFF'
        self.theme_background_color = '#8A42AA'
        self.theme_admin_background_color = '#8F222D'
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


def get_cart_item_list(request):
    """..."""
    try:
        return models.ModelCart.objects.filter(user=request.user)
    except Exception as err:
        logging.error(err)
        return []


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
