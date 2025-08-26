from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base import AuthorsBaseTest
from selenium.webdriver.common.by import By
from django.urls import reverse


class AuthorsLoginTest(AuthorsBaseTest):
    def test_loging_with_valid_user(self):
        self.get_browser('cadastro')
        form = self.get_form()
        self.sleeps(2)

        self.creat_user_for_tests()
        form.submit()

        form = self.get_form()
        self.loging_user_for_test()
        form.submit()

        body = WebDriverWait(self.browser, 5).until(EC.text_to_be_present_in_element((By.TAG_NAME, 'body'),'Bem Vindo firstlast !'))

        self.assertTrue(body)

    def test_login_with_invalid_user(self):
        self.get_browser('login')
        form = self.get_form()
        self.sleeps(2)

        self.loging_user_for_test()
        form.submit()

        self.assertIn('Usuario ou senha incorretos', self.browser.find_element(By.TAG_NAME, 'body').text)

    def test_form_login_is_invalid(self):
        self.get_browser('login')
        form = self.get_form()
        self.sleeps(2)

        self.get_by_placeholder('Usuário', '  ')
        self.get_by_placeholder('Senha', '  ')
        form.submit()

        self.assertIn('Usuario ou senha incorretos', self.browser.find_element(By.TAG_NAME, 'body').text)

    def test_loging_create_raise_404_if_not_post_method(self):
        self.browser.get(self.live_server_url + reverse('authors:login_create'))
        self.assertIn('Pagina Não Encontrada', self.browser.find_element(By.TAG_NAME, 'body').text)

    def test_logout_user(self):
        self.get_browser('cadastro')
        self.sleeps(2)
        form = self.get_form()
        self.creat_user_for_tests()
        form.submit()
        form = self.get_form()
        self.loging_user_for_test()
        form.submit()

        btn_sair = self.browser.find_element(By.TAG_NAME, 'button')
        btn_sair.click()

        self.assertIn('LOGIN', self.browser.find_element(By.TAG_NAME, 'body').text)



