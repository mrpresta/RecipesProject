from django.test import TestCase
from django.urls import reverse

class RecipeURLsTest(TestCase):
    def test_recipe_home_url_is_correct(self):
        url = reverse('recipes:home')
        self.assertEqual(url, '/')

    def test_recipes_category_url_is_correct(self):
        url = reverse('recipes:category', kwargs={'category_id':1})
        self.assertEqual(url, '/recipes/category/1/')

    def test_recipes_detail_url_is_correcet(self):
        url = reverse('recipes:recipe_detail', kwargs={'id':1})
        self.assertEqual(url, '/recipes/1/')
