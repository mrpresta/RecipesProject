import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()

def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)

def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{6,}$')

    if not regex.match(password):
        raise ValidationError((
            'Senha pracisa ter uma letra maiuscula, uma minuscula, um numero e ter pelo menos 6 caracteres'
        ),
            code='Invalid'
        )

class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_placeholder(self.fields['first_name'], 'Nome')
        add_placeholder(self.fields['last_name'], 'Sobrenome')
        add_placeholder(self.fields['email'], 'E-mail')
        add_placeholder(self.fields['username'], 'Usuario')
        add_placeholder(self.fields['password'], 'Senha')

    password = forms.CharField(
        required=True,
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'placeholder':'Senha'
        }),
        error_messages={
            'required':'* campo obrigratorio'
        },
        validators = [strong_password]
    )

    password_confimation = forms.CharField(
        required=True,
        label='Confirme sua Senha',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirme sua Senha'
        }),
        error_messages={
            'required': ''
        },
        validators=[strong_password]
    )

    class Meta:
        model =  User
        fields = ['first_name',
                  'last_name',
                  'email',
                  'username',
                  'password']

        help_texts = {
            'username': ' '
        }

    def clean_password(self):
        data = self.cleaned_data.get('password')

        if 'atenção' in data:
            raise ValidationError(
                'Não digite atenção no campo password',
                code='invalid'
            )
        return data

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confiomation_password = cleaned_data.get('password_confimation')

        if password != confiomation_password:
            raise ValidationError({
                'password': 'A Senha e a Confirmação precisam ser iguais',
                'password_confimation': 'A Senha e a Confirmação precisam ser iguais'
            }
            )
        return


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username',
                  'password']