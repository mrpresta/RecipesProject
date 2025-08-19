from recipes import views
from django.urls import reverse, resolve
from .test_recipe_base import RecipeTestBase
from recipes.models import Recipe


class RecipeSearchViewsTest(RecipeTestBase):
    #testes de function view
    def test_recipe_search_view_function_is_correct(self):
        view = resolve(reverse('recipes:search'))
        self.assertIs(view.func, views.search)

    #testes de status code 200
    def test_recipe_detail_view_returns_status_code_200_ok(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:recipe_detail', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)

    #testes de carregamento de template correto
    def test_recipe_search_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search')+'?q=teste')
        self.assertTemplateUsed(response, 'recipes/search_view.html')

    #teste de carregamente de receita no tamplate

    #testes de carregamento template 404

    #teste se is_published = false retorna o 404


    def test_recipe_search_raises_404_if_no_search_term(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_escaped(self):
        response = self.client.get(reverse('recipes:search') + '?q=<teste>')
        self.assertIn('q &quot;&lt;teste&gt;&quot;', response.content.decode('utf-8'))

    def test_recipe_search_can_find_recipe_by_title(self):
        title1 = 'this is title one'
        title2 = 'this is title two'

        recipe1 = self.make_recipe(slug='one', tittle=title1, author=self.make_user(username='user1'))
        recipe2 = self.make_recipe(slug='two', tittle=title2, author=self.make_user(username='user2'))

        url = reverse('recipes:search')

        response1 = self.client.get(f'{url}?q={title1}')
        response2 = self.client.get(f'{url}?q={title2}')
        response_both = self.client.get(f'{url}?q=this')

        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])

        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])


