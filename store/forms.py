from django import forms
from users.models import ModelUser


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
