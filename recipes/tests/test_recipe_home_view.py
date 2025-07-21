from recipes import views
from django.urls import reverse, resolve
from .test_recipe_base import RecipeTestBase
from recipes.models import Recipe


class RecipeHomeViewsTest(RecipeTestBase):
    #testes de function view
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)
   #testes de status code 200
    def test_recipe_home_view_returns_status_code_200_ok(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)
    #testes de carregamento de template correto
    def test_recipe_home_view_loads_correct_template(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/home.html')
#teste de carregamente de receita no tamplate
    def test_recipe_home_templates_load_recipe(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipe = response.context['recipes']
        #chega se existe receitas no template
        self.assertIn('Minha Receita Teste', content)
        self.assertEqual(len(response_context_recipe), 1)

    # testes de carregamento template 404
    def test_recipe_404_loads_correct_template_if_not_have_recipes_in_home(self):
        Recipe.objects.all().delete()
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, '404.html')

    # teste se is_published = false retorna o 404
    def test_recipe_home_template_dont_load_recipes_not_published(self):
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('<h1> Pagina Não Encontrada </h1>', response.content.decode('utf-8'))
        self.assertTemplateUsed(response, '404.html')