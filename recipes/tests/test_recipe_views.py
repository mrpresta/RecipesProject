from recipes import views
from django.urls import reverse, resolve
from .test_recipe_base import RecipeTestBase
from recipes.models import Recipe


class RecipeViewsTest(RecipeTestBase):
    #testes de function view
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id':1}))
        self.assertIs(view.func, views.category)

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe_detail', args=(1,)))
        self.assertIs(view.func, views.recipes)

    #testes de status code 200
    def test_recipe_home_view_returns_status_code_200_ok(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_category_view_returns_status_code_200_ok(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertEqual(response.status_code, 200)

    def test_recipe_detail_view_returns_status_code_200_ok(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:recipe_detail', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)

    #testes de carregamento de template correto
    def test_recipe_home_view_loads_correct_template(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/home.html')

    def test_recipe_category_view_loads_correct_template(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertTemplateUsed(response, 'recipes/category.html')

    def test_recipe_detail_view_loads_correct_template(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:recipe_detail', kwargs={'id': 1}))
        self.assertTemplateUsed(response, 'recipes/recipes_description.html')

    #teste de carregamente de receita no tamplate
    def test_recipe_home_templates_load_recipe(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipe = response.context['recipes']

        #chega se existe receitas no template
        self.assertIn('Minha Receita Teste', content)
        self.assertEqual(len(response_context_recipe), 1)

    def test_recipe_category_templates_load_recipe(self):
        test_title = 'teste receitas no template category'
        self.make_recipe(tittle=test_title)
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1}))
        content =  response.content.decode('utf-8')

        # checa se recebe a receita correta com o titulo certo  no template
        self.assertIn('teste receitas no template category', content)

    def test_recipe_detail_templates_load_the_correct_recipe(self):
        test_title = 'Teste titulo buscando na pagina de receita detalhada '
        self.make_recipe(tittle= test_title)
        response = self.client.get(reverse('recipes:recipe_detail', kwargs={'id': 1}))
        content = response.content.decode('utf8')

        # checa se recebe a receita correta com o titulo certo  no template
        self.assertIn('Teste titulo buscando na pagina de receita detalhada', content)

    #testes de carregamento template 404
    def test_recipe_404_loads_correct_template_if_not_have_recipes_in_home(self):
        Recipe.objects.all().delete()
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, '404.html')

    def test_recipe_404_loads_correct_template_if_not_have_recipes_in_category(self):
        Recipe.objects.all().delete()
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 999}))
        self.assertTemplateUsed(response, '404.html')

    def test_recipe_404_loads_correct_template_if_not_have_recipes_in_recipe(self):
        response = self.client.get(reverse('recipes:recipe_detail', kwargs={'id': 999}))
        self.assertTemplateUsed(response, '404.html')

    #teste se is_published = false retorna o 404
    def test_recipe_home_template_dont_load_recipes_not_published(self):
        self.make_recipe(is_published = False)
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('<h1> Pagina Não Encontrada </h1>', response.content.decode('utf-8'))
        self.assertTemplateUsed(response, '404.html')

    def test_recipe_category_template_dont_load_recipe_not_published(self):
        self.make_recipe(is_published = False)
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIn('<h2>Voltar a Pagina Principal</h2>', response.content.decode('utf-8'))
        self.assertTemplateUsed(response, '404.html')

    def test_recipe_detail_template_dont_load_recipe_not_published(self):
        self.make_recipe(is_published = False)
        response = self.client.get(reverse('recipes:recipe_detail', kwargs={'id': 1}))
        self.assertIn('<h1> Pagina Não Encontrada </h1>', response.content.decode('utf-8'))
        self.assertTemplateUsed(response, '404.html')