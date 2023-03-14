from django import forms
from users.models import ModelUser
from store.models import ModelProduct, ModelUserProfile, ModelStoreProfile


class FormLogin(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ModelUser
        fields = ['username', 'password']
        labels = {
            'username': '<h6>Nome de usuário</h6>',
            'password': '<h6>Senha</h6>',
        }
        widgets = {
            'password': forms.PasswordInput(),
        }


class FormProductNew(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for visible in self.visible_fields():
            if (visible.name == 'is_published' or
                    visible.name == 'price_off_display' or
                    visible.name == 'available_quantity_display'):

                visible.field.widget.attrs['class'] = 'form-check-input'
            else:
                visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ModelProduct
        exclude = [
            'user', 'title_for_card', 'title_for_url', 'price_pprint',
            'price_old', 'price_old_pprint', 'price_off', 'price_off_pprint',
            'times_split_unit', 'times_split_pprint', 'shipping_price_pprint',
            'publication_date']
        # fields = '__all__'
        labels = {
            'title': '<h6>Título</h6>',
            'price': '<h6>Preço</h6>',
            'price_off_display': 'Mostrar preço OFF',
            'times_split_num': '<h6>Dividir em quantas vezes</h6>',
            'times_split_interest': '<h6>Porcento de juros sobre total</h6>',
            'shipping_price': '<h6>Preço do frete</h6>',
            'available_quantity': '<h6>Quantos disponíveis</h6>',
            'available_quantity_display':
                '<h6>Mostrar a quantidade disponível</h6>',
            'max_quantity_per_sale': '<h6>Máximo de itens por cada venda</h6>',
            'image_1': '<h6>Imagem principal&nbsp;</h6>',
            'image_2': (
                '<h6>Imagem 2'
                '<small class="text-muted"> (Opcional)&nbsp;</small></h6>'),
            'image_3': (
                '<h6>Imagem 3'
                '<small class="text-muted"> (Opcional)&nbsp;</small></h6>'),
            'image_4': (
                '<h6>Imagem 4'
                '<small class="text-muted"> (Opcional)&nbsp;</small></h6>'),
            'image_5': (
                '<h6>Imagem 5'
                '<small class="text-muted"> (Opcional)&nbsp;</small></h6>'),
            'summary': '<h6>Resumo</h6>',
            'content': '<h6>Decrição</h6>',
            'tags': '<h6>Tags</h6>',
            'is_published': (
                '<h6>Marcar como publicado '
                '<small class="text-muted">(Visível ao público)</small></h6>'),
        }


class FormSignup(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ModelUser
        fields = '__all__'
        labels = {
            'name': '<h6>Nome</h6>',

            'username': (
                '<h6>Nome de usuário</h6>'
                '<small class="text-muted">'
                'Pode conter letra minúscula e número'
                '</small>'),

            'email': '<h6>Email</h6>',

            'password': (
                '<h6>Senha</h6>'
                '<small class="text-muted">'
                'Precisa conter letra, número e caractere especial'
                '</small>'),

            'password_confirm': '<h6>Senha novamente</h6>',
        }
        widgets = {
            'password': forms.PasswordInput(),
            'password_confirm': forms.PasswordInput(),
        }


class FormStoreProfile(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.field.widget.input_type == 'checkbox':
                visible.field.widget.attrs['class'] = 'form-check-input'
            else:
                visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ModelStoreProfile
        exclude = ['owner', 'background_color', 'theme_color_admin']
        labels = {
            'brand_name': '<h6>Nome da loja</h6>',
            'show_brand_name_on_nav': '<h6>&nbsp;Exibir nome da loja</h6>',
            'brand_image': '<h6>Imagem da logo</h6>',
            'show_brand_image_on_nav': '<h6>&nbsp;Exibir imagem da logo</h6>',
            'theme_color': '<h6>Cor de destaque da loja</h6>',
            'theme_color_text': '<h6>Cor do texto na cor de destaque</h6>',
            'social_media_facebook': '<h6>Link do Facebook</h6>',
            'social_media_whatsapp': '<h6>Link do WhatsApp</h6>',
            'social_media_twitter': '<h6>Link do Twitter</h6>',
            'social_media_youtube': '<h6>Link do YouTube</h6>',
            'social_media_instagram': '<h6>Link do Instagram</h6>',
            'social_media_twitch': '<h6>Link da Twitch</h6>',
            'social_media_discord': '<h6>Link do Discord</h6>',
            'social_media_linkedin': '<h6>Link do LinkedIn</h6>',
            'social_media_github': '<h6>Link do GitHub</h6>',
            'social_media_other': '<h6>Link de outra página da web</h6>',
        }


class FormUserEdit(forms.ModelForm):
    password = forms.CharField(
        required=False,
        label='<h6>Senha atual</h6>')
    password_confirm = forms.CharField(
        required=False,
        label=('<h6>Nova Senha</h6>'
               '<small class="text-muted">'
               'Adicinar uma senha aqui, alterará a senha atual.<br>'
               'A senha precisa conter letra, número e caractere especial'
               '</small>'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ModelUser
        fields = '__all__'
        labels = {
            'name': '<h6>Nome</h6>',
            'username': (
                '<h6>Nome de usuário</h6>'
                '<small class="text-muted">'
                'Pode conter letra minúscula e número'
                '</small>'),
            'email': '<h6>Email</h6>'}


class FormUserProfileEdit(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.name == 'is_admin' or visible.name == 'is_blocked':
                visible.field.widget.attrs['class'] = 'form-check-input'
            else:
                visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ModelUserProfile
        fields = ['profile_image', 'is_blocked']
        labels = {
            'profile_image': '<h6>Imagem de perfil&nbsp;</h6>',
            'is_blocked': '<h6>Suspender conta</h6>',
        }


class FormUserDashboard(forms.ModelForm):
    password = forms.CharField(
        required=False,
        label=(
            '<h3 class="my-3">Senha</h3>'
            '<h6>Senha atual</h6>'
            '<small class="text-muted">'
            'A senha atual é usada para confirmar a nova senha<br>'
            '</small>'))
    password_confirm = forms.CharField(
        required=False,
        label=(
            '<h6>Nova senha</h6>'
            '<small class="text-muted">'
            'Precisa conter letras, números e caracteres especiais'
            '</small>'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ModelUser
        fields = '__all__'
        labels = {
            'name': '<h3 class="my-3">Conta</h3><h6>Nome</h6>',
            'username': (
                '<h6>Nome de usuário</h6>'
                '<small class="text-muted">'
                'Pode conter letra minúscula e número'
                '</small>'),
            'email': '<h6>Email</h6>'}


class FormUserDashboardProfile(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.field.widget.input_type == 'checkbox':
                visible.field.widget.attrs['class'] = 'form-check-input'
            else:
                visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ModelUserProfile
        fields = ['profile_image']
        labels = {
            'profile_image': (
                '<h3 class="my-3">Perfil</h3><h6>Imagem de perfil&nbsp;</h6>')}
