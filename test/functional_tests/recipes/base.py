from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_chrome_browser
from recipes.tests.test_recipe_base import RecipeMixin
import time

class RecipeBaseFunctionTest(StaticLiveServerTestCase, RecipeMixin):
    def setUp(self):
        self.browser = make_chrome_browser('--headless')
        return super().setUp()

    def setUp_with_recipes(self, qtd=10):
        self.make_recipe_in_batch(qtd=qtd)

    def tearDown(self):
        self.browser.quit()
        return super().tearDown()

    def sleeps(self, seconds=5):
        time.sleep(seconds)