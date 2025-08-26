from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from .base import RecipeBaseFunctionTest
from unittest.mock import patch
import pytest

@pytest.mark.functional_test
class RecipeHomePagefunctionalTest(RecipeBaseFunctionTest):
    def test_the_test(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Pagina Não Encontrada', body.text)

    @patch('recipes.views.PER_PAGE', new = 5)
    def test_recipes_homepage_withoput_recipes_raise_page_404_text_body(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Pagina Não Encontrada', body.text)

    @patch('recipes.views.PER_PAGE', new = 5)
    def test_recipes_search_input_can_find_correct_recipes(self):
        self.setUp_with_recipes(qtd=10)
        self.browser.get(self.live_server_url)
        search_input = self.browser.find_element(By.XPATH, '//input[@placeholder="Qual receita esta procurando"]')
        self.sleeps()
        search_input.click()
        self.sleeps()
        search_input.send_keys('Teste2')
        search_input.send_keys(Keys.ENTER)

        self.assertIn('Teste2', self.browser.find_element(By.TAG_NAME, 'body').text)

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipes_pagination(self):
        self.setUp_with_recipes(qtd=10)
        self.browser.get(self.live_server_url)
        self.sleeps()
        page2 = self.browser.find_element(By.XPATH, '//a[@aria-label="Go to page 2"]')
        page2.click()
        self.assertEqual(len(self.browser.find_elements(By.CLASS_NAME, 'recipe')), 2)


