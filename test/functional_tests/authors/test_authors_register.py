from .base import AuthorsBaseTest
from selenium.webdriver.common.by import By

class AuthorsRegisterTest(AuthorsBaseTest):
    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')
        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)

    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + '/cadastro/')
        self.sleeps(2)
        form = self.get_form()

        self.fill_form_dummy_data(form)
        form.find_element(By.NAME, 'email').send_keys('dummy@email.com')

        callback(form)
        return form

    def test_empty_fields_messages(self):
        def callback(form):
            first_name_field = self.get_by_placeholder('Nome')
            first_name_field.submit()
            form = self.get_form()

            self.assertIn('O campo precisa conter seu nome', form.text)
            self.assertIn('O campo precisa conter seu sobrenome', form.text)
            self.assertIn('O campo nao pode ser vazio', form.text)
            self.assertIn('* campo obrigratorio', form.text)
        self.form_field_test_with_callback(callback)

    def test_user_valid_data_register(self):
        self.browser.get(self.live_server_url + '/cadastro/')
        form = self.get_form()

        self.creat_user_for_tests()
        form.submit()

        self.assertIn('Você foi cadastrado com sucesso', self.browser.find_element(By.TAG_NAME, 'body').text)
