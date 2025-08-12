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
            'A Senha pracisa ter 1 letra maiuscula, 1 minuscula, 1 numero e ter pelo menos 6 caracteres'
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

    first_name = forms.CharField(
        required=True,
        error_messages={'required': 'O campo precisa conter seu nome'},
        label='Nome'
    )

    last_name = forms.CharField(
        required=True,
        error_messages={'required': 'O campo precisa conter seu sobrenome'},
        label='Sobrenome'
    )

    email = forms.EmailField(
        required=True,
        error_messages={'required': 'E-mail precisa ser valido'},
        label='E-mail',
        help_text='',
    )

    username = forms.CharField(
        required=True,
        error_messages={'required':'O campo nao pode ser vazio',
                        'min_length':'O usuario deve ter pelo menos 4 caracteres',
                        'max_length':'O usuario deve ter menos de 150 caracteres'
        },
        help_text='',
        label='Usuário',
        min_length=4,
        max_length=50,
    )

    password = forms.CharField(
        required=True,
        label='Senha',
        widget=forms.PasswordInput(attrs={
        }),
        error_messages={
            'required':'* campo obrigratorio',
        },
        validators = [strong_password]
    )

    password_confirmation = forms.CharField(
        required=True,
        label='Confirme sua Senha',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirme sua Senha'
        }),
        error_messages={
            'required': '* campo obrigratorio'
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

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'Email já cadastrado', code='invalid',
            )
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confiomation_password = cleaned_data.get('password_confirmation')

        if password != confiomation_password:
            raise ValidationError({
                'password': 'A Senha e a Confirmação precisam ser iguais',
                'password_confirmation': 'A Senha e a Confirmação precisam ser iguais'
            }
            )
        return


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username',
                  'password']