from .test_recipe_base import RecipeTestBase, Recipe
from django.core.exceptions import ValidationError
from parameterized import parameterized


class RecipeModelTest(RecipeTestBase):
    def setUp(self):
        super().setUp()
        self.recipe = self.make_recipe()

    def make_recipe_no_default(self):
        recipe = Recipe(
            category=self.make_category(name='Teste default model'),
            author=self.make_user(username='TesteDefaultModel', first_name='TesteDefault', last_name='Model',
                                  password='testedefaultmodel', email='testedefaultmodel@gmail.com'),
            tittle='Receita teste default model',
            description='teste default model',
            slug='Receite-teste-default-model',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings_steps=2,
            servings_steps_unit='Pessoas',
            preparation_steps='Passos de preparo',
        )
        recipe.full_clean()
        recipe.save()
        return recipe

    @parameterized.expand([
            ('tittle', 65),
            ('description', 165),
            ('preparation_time_unit', 65),
            ('servings_steps_unit', 65),
        ])
    #testes de max_length atributos da colunas do model de receitas
    def test_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, 'a' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    # testes de max_length atributos da colunas do model de Categorias



    #teste de default
    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_default()
        self.assertFalse(recipe.preparation_steps_is_html)

    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_default()
        self.assertFalse(recipe.is_published)

    #testes de representação de string do Recipe
    def test_recipe_string_representation(self):
        self.recipe.tittle ='Testing Representation'
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(str(self.recipe), f'{self.category}: {self.recipe.tittle}')


