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





