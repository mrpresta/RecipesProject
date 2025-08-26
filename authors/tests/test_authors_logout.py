from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class AuthorsLogoutTest(TestCase):
    def test_user_tries_logout_using_get_method(self):
        User.objects.create_user(username='my_user_test', password='My_pass12')
        self.client.login(username='my_user_test', password='My_pass12')

        response = self.client.get(reverse('authors:logout'), follow=True)

        self.assertIn('Invalid request', response.content.decode('utf-8'))


    def test_user_tries_logout_another_user(self):
        User.objects.create_user(username='my_user_test', password='My_pass12')
        self.client.login(username='my_user_test', password='My_pass12')

        response = self.client.post(reverse('authors:logout'), data={'username':'another_user'}, follow=True)

        self.assertIn('Divergent User', response.content.decode('utf-8'))

    def test_user_logout_success(self):
        User.objects.create_user(username='my_user_test', password='My_pass12')
        self.client.login(username='my_user_test', password='My_pass12')

        response = self.client.post(reverse('authors:logout'), {'username': 'my_user_test'}, follow=True)

        self.assertIn('Logout User', response.content.decode('utf-8'))
