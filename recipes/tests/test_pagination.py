from django.test import TestCase,RequestFactory
from utils.pagination import make_pagination_range, make_pagination
from recipes.models import Recipe


class PaginationTeste(TestCase):
    def test_make_pagination_range_renturns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range = list(range(1,21)),
            qty_pages = 4,
            current_page = 1,
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

    def test_first_range_is_static_if_current_page_is_lass_then_middle_page(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1,
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=2,
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=3,
        )['pagination']
        self.assertEqual([2, 3, 4, 5], pagination)

    def test_make_sure_middle_ranges_are_correct(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=10,
        )['pagination']
        self.assertEqual([9, 10, 11, 12], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=12,
        )['pagination']
        self.assertEqual([11, 12, 13, 14], pagination)


    def test_final_range_is_correct_when_current_page_is_near_the_end(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=18,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=19,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=20,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

class PaginationExceptTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        for i in range(10):
            Recipe.objects.create(tittle=f'Recipe{i}', slug=f'slug-{i}', preparation_time=1,servings_steps=1)

    def test_if_except_value_error_is_1_when_dont_convert_in_int(self):
        request = self.factory.get('/fake-url/?page=banana')
        queryset = Recipe.objects.all().order_by('-id')
        page_object, pagination_range = make_pagination(request, queryset, per_page=2, qty_page=4)

        self.assertEqual(page_object.number, 1)
        self.assertEqual(pagination_range['current_page'], 1)

