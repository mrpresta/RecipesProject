from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_chrome_browser
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

class AuthorsBaseTest(StaticLiveServerTestCase):
    def setUp(self)-> None:
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def sleeps(self, seconds=5):
        time.sleep(seconds)

    def get_browser(self, pageurl):
        self.browser.get(self.live_server_url + f'/{pageurl}/')

    def get_by_placeholder(self, placeholder, value=None):
        element = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, f"//input[@placeholder='{placeholder}']")))

        if value is not None:
            element.send_keys(value)
        return element

    def get_form(self):
        return self.browser.find_element(By.XPATH,'/html/body/div/form')

    def creat_user_for_tests(self):
        self.get_by_placeholder('Nome', 'First')
        self.get_by_placeholder('Sobrenome', 'Last')
        self.get_by_placeholder('E-mail', 'firstLast@gmail.com')
        self.get_by_placeholder('Usuario', 'firstlast')
        self.get_by_placeholder('Senha', 'First12')
        self.get_by_placeholder('Confirme sua Senha', 'First12')

    def loging_user_for_test(self):
        self.get_by_placeholder('Usuário', 'firstlast')
        self.get_by_placeholder('Senha', 'First12')