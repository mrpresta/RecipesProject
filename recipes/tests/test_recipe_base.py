from django.test import TestCase
from recipes.models import Recipe, Category
from django.contrib.auth.models import User

class RecipeTestBase(TestCase):
    def setUp(self):
        # Cria User e Category para a Recipe
        self.user = self.make_user()
        self.category = self.make_category()

        # a receita vai ser criada a cada teste que precise de
        # receita resultando em economia de tempo

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
            tittle='Minha Receita Teste',
            description='Descrição teste',
            slug='minha-receita-teste',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings_steps=2,  # <-- nome real
            servings_steps_unit='Pessoas',  # <-- nome real
            preparation_steps='Passos de preparo',
            preparation_steps_is_html=False,
            is_published=True
    ):
        return Recipe.objects.create(
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
            author=self.user,
            category=self.category
        )