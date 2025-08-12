from django.test import TestCase as DjangoTestCase
from unittest import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized
from django.urls import reverse

class AuthorRegisterFormsUnitTest(TestCase):
    @parameterized.expand([
        ('first_name', 'Nome'),
        ('last_name', 'Sobrenome'),
        ('email', 'E-mail'),
        ('username', 'Usuario'),
        ('password', 'Senha'),
        ('password_confirmation', 'Confirme sua Senha'),
    ])
    def test_fields_placeholder_is_correct(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder, placeholder)

    def test_help_text_usarname_is_correct(self):
        form = RegisterForm()
        current = form['username'].field.help_text
        self.assertEqual(current, '')

    @parameterized.expand([
        ('first_name', 'Nome'),
        ('last_name','Sobrenome'),
        ('email','E-mail'),
        ('username', 'Usuário'),
        ('password', 'Senha'),
        ('password_confirmation', 'Confirme sua Senha'),
    ])
    def test_fields_labels_is_correct(self, field, label):
        form = RegisterForm()
        current_label = form[field].field.label
        self.assertEqual(current_label, label)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'first_name': 'First',
            'last_name':'Last',
            'email':'email@email.com',
            'username': 'User',
            'password': 'Pass123',
            'password_confirmation': 'Pass123',
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'O campo nao pode ser vazio'),
        ('first_name', 'O campo precisa conter seu nome'),
        ('last_name', 'O campo precisa conter seu sobrenome'),
        ('password', '* campo obrigratorio'),
        ('password_confirmation', '* campo obrigratorio'),
        ('email', 'E-mail precisa ser valido'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))

    def test_usarname_field_min_length_should_be_4(self):
        self.form_data['username'] = 'fel'
        url = reverse('authors:create')
        msg = 'O usuario deve ter pelo menos 4 caracteres'
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_usarname_field_max_length_should_be_lass_than_150(self):
        self.form_data['username'] = 'a' * 151
        url = reverse('authors:create')
        msg = 'O usuario deve ter menos de 150 caracteres'
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_password_field_have_lower_upper_number(self):
        self.form_data['password'] = 'felipe'
        url = reverse('authors:create')
        msg = 'A Senha pracisa ter 1 letra maiuscula, 1 minuscula, 1 numero e ter pelo menos 6 caracteres'
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))

    def test_password_and_confirmation_are_equal(self):
        self.form_data['password'] = 'Felipe12'
        self.form_data['password_confirmation'] = 'Felipe09'
        url = reverse('authors:create')
        msg = 'A Senha e a Confirmação precisam ser iguais'
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.assertIn(msg, response.context['form'].errors.get('password_confirmation'))

    def test_send_get_request_to_registration_create_view_returns_404(self):
        url = reverse('authors:create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_email_is_unique(self):
        url = reverse('authors:create')
        self.client.post(url, data=self.form_data, follow=True)
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Email já cadastrado'

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('email'))

    def teste_author_created_can_login(self):
        url = reverse('authors:create')

        self.form_data.update({
            'username':'usertest',
            'password':'1Testuser',
            'password_confirmation':'1Testuser',
        })
        self.client.post(url, data=self.form_data, follow=True)

        is_authenticated = self.client.login(
            username='usertest',
            password='1Testuser',
        )

        self.assertTrue(is_authenticated)