from .test_recipe_base import RecipeTestBase
from django.core.exceptions import ValidationError

class CategoryModelTest(RecipeTestBase):
    def setUp(self):
        self.category = self.make_category(name='Category Test')
        super().setUp()

    #teste max_length category
    def test_category_model_name_max_length_is_65_char(self):
        self.category.name = 'a'* 70
        with self.assertRaises(ValidationError):
            self.category.full_clean()

    # testes de representação de string do Category
    def test_category_string_representation(self):
        self.assertEqual(str(self.category), self.category.name)

