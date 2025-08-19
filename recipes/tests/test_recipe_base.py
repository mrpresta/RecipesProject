from django.template.base import kwarg_re
from django.test import TestCase
from recipes.models import Recipe, Category
from django.contrib.auth.models import User

class RecipeMixin:
    def make_category(self, name='Categoria Teste'):
        return Category.objects.create(name=name)

    def make_user(
            self,
            first_name='Test',
            last_name='User',
            username='testuser',
            password='testpass',
            email='testemail@testemail.com'
    ):

        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )
    def make_recipe(
            self,
            category = None,
            author = None,
            tittle='Minha Receita Teste',
            description='Descrição teste',
            slug='minha-receita-teste',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings_steps=2,
            servings_steps_unit='Pessoas',
            preparation_steps='Passos de preparo',
            preparation_steps_is_html=False,
            is_published=True

    ):
        if category is None:
            category = self.make_category()
        if author is None:
            author = self.make_user()

        return Recipe.objects.create(
            category=category,
            author=author,
            tittle=tittle,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings_steps=servings_steps,
            servings_steps_unit=servings_steps_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published,
        )

    def make_recipe_in_batch(self, qtd=10):
        recipes = []
        for i in range(qtd):
            user = self.make_user(username=f'u{i}')
            kwarg = {'slug': f'r{i}', 'author':user}
            recipe = self.make_recipe(**kwarg)
            recipes.append(recipe)
        return recipes

class RecipeTestBase(TestCase, RecipeMixin):
    def setUp(self) -> None:
        return super().setUp()

