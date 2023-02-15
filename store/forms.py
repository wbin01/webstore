from django import forms
from users.models import ModelUser
from store.models import ModelProduct


class FormLogin(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ModelUser
        fields = ['username', 'password']
        # fields = '__all__'
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
            # '': '<h6></h6>',
        }
        # widgets = {
        #     'password': forms.PasswordInput(),
        # }


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
