from .test_recipe_base import RecipeTestBase
from django.core.exceptions import ValidationError
from parameterized import parameterized


class RecipeModelTest(RecipeTestBase):
    def setUp(self):
        super().setUp()
        self.recipe = self.make_recipe()

    @parameterized.expand([
            ('tittle', 65),
            ('description', 165),
            ('preparation_time_unit', 65),
            ('servings_steps_unit', 65),
        ])
    def test_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, 'a' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()