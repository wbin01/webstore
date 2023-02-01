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
            'username': 'Nome de usuário',
            'password': 'Senha',
        }
        widgets = {
            'password': forms.PasswordInput(),
        }

    # def clean(self):
    #     fields = {
    #         'username': self.cleaned_data.get('username'),
    #         'password': self.cleaned_data.get('password')}
    #
    #     errors = {}
    #
    #     for key, value in fields.items():
    #         if not value.strip():
    #             errors[key] = 'Preencha este campo'
    #
    #     if not fields['username'].isalpha():
    #         errors['name'] = 'Só é permitido letras neste campo'
    #
    #     if errors:
    #         for erro in errors:
    #             error_message = errors[erro]
    #             self.add_error(erro, error_message)
    #     return self.cleaned_data
