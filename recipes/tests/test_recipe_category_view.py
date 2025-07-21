from recipes import views
from django.urls import reverse, resolve
from .test_recipe_base import RecipeTestBase
from recipes.models import Recipe


class RecipeCategoryViewsTest(RecipeTestBase):
    #testes de function view
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id':1}))
        self.assertIs(view.func, views.category)

    # testes de status code 200
    def test_recipe_category_view_returns_status_code_200_ok(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertEqual(response.status_code, 200)

    # testes de carregamento de template correto
    def test_recipe_category_view_loads_correct_template(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertTemplateUsed(response, 'recipes/category.html')

        # teste de carregamente de receita no tamplate
    def test_recipe_category_templates_load_recipe(self):
        test_title = 'teste receitas no template category'
        self.make_recipe(tittle=test_title)
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1}))
        content = response.content.decode('utf-8')

        # checa se recebe a receita correta com o titulo certo  no template
        self.assertIn('teste receitas no template category', content)

    #testes de carregamento template 404
    def test_recipe_404_loads_correct_template_if_not_have_recipes_in_category(self):
        Recipe.objects.all().delete()
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 999}))
        self.assertTemplateUsed(response, '404.html')

    # teste se is_published = false retorna o 404
    def test_recipe_category_template_dont_load_recipe_not_published(self):
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIn('<h2>Voltar a Pagina Principal</h2>', response.content.decode('utf-8'))
        self.assertTemplateUsed(response, '404.html')




