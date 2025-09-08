import re
from idlelib.debugobj import myrepr

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from recipes.models import Recipe, Category
from collections import defaultdict

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


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_placeholder(self.fields['username'], 'Usuário')
        add_placeholder(self.fields['password'], 'Senha')

    username = forms.CharField(
        label='Usuário'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label='Senha'
    )

class CadastrarReceitaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.my_errors = defaultdict(list)



        add_placeholder(self.fields['tittle'], 'Titulo')
        add_placeholder(self.fields['description'], 'Descrição')
        add_placeholder(self.fields['cover'], 'Capa')
        add_placeholder(self.fields['category'], 'Categoria')
        add_placeholder(self.fields['preparation_time'], 'Tempo de Preparo')
        add_placeholder(self.fields['servings_steps'], 'Quantas Porções Rendem')
        add_placeholder(self.fields['preparation_time_unit'], 'Ex.: Minutos, Hora, Horas')
        add_placeholder(self.fields['preparation_steps'], 'Ingrediente e Passo a Passo de Preparo')


    class Meta:
        model = Recipe
        fields = ['tittle','description', 'category', 'preparation_time', 'preparation_time_unit', 'servings_steps','cover', 'preparation_steps' ]

    tittle = forms.CharField(
        required=True,
        label= 'Titulo da Receita',
        error_messages={
            'required': '* campo obrigratorio'
        }
    )

    description = forms.CharField(
        required=True,
        label='Descrição ',
    )

    porcoes_choices = [(porcoes, str(porcoes)) for porcoes in range(1, 21)]

    servings_steps = forms.ChoiceField(
        required=True,
        label='Quantidade de Rendimento',
        choices=porcoes_choices,
    )
    tempo_choices = [(porcoes, str(porcoes)) for porcoes in range(1, 61)]
    preparation_time = forms.ChoiceField(
        label='Tempo de preparo',
        choices=tempo_choices
    )

    preparation_time_unit = forms.CharField(
        required=True,
        label='Unidade de Tempo de Preparo',
        widget = forms.Select(
            choices=(
                ('minutos', 'Minutos'),
                ('horas', 'Horas'),
            )
        )
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=True,
        label='Categoria',
        empty_label='Selecione a categoria',
    )

    preparation_steps = forms.CharField(
        required=True,
        label='Ingredientes e Passo a Passo',
        widget=forms.Textarea()
    )

    def clean(self):
        super_clean = super().clean()

        cleanded_data = self.cleaned_data
        tittle = super_clean.get('tittle')
        description = super_clean.get('description')


        if len(tittle) < 5:
            self.my_errors['tittle'].append('Deve ao menos 5 catacteres')

        if tittle == description:
            self.my_errors['tittle'].append('Titulo nao deve ser igual a Descrição')
            self.my_errors['description'].append('Descrição nao deve ser igual ao Titulo ')






        if self.my_errors:
            raise ValidationError(self.my_errors)
        return super_clean

