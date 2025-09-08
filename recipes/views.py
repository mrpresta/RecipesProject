from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.db.models import Q
from .models import Recipe
from django.http import Http404
from utils.pagination import make_pagination
import os

# Create your views here.
PER_PAGE = os.environ.get('PER_PAGE', 3)

def home(request):
    recipes = get_list_or_404(Recipe.objects.order_by('-id'), is_published=True)

    page_object, pagination_range =  make_pagination(request, recipes, PER_PAGE)
    page = request.GET.get('page', 1)
    return render(request, 'recipes/home.html', context={
        'recipes': page_object,
        'pagination_range': pagination_range,
        'page': page,
    })

def category(request, category_id):
    recipes = get_list_or_404(Recipe.objects.order_by('-id'), category__id=category_id, is_published=True)
    page_object, pagination_range = make_pagination(request, recipes, PER_PAGE)



    return render(request, 'recipes/category.html', context={
        'recipes': page_object,
        'pagination_range':pagination_range,
        'title': f'{recipes[0].category.name} | Category',

    })

def recipes(request, id):
    page = request.GET.get('page', 1)

    if request.user.is_authenticated:
        recipe = get_object_or_404(
            Recipe,
            Q(id=id) & (Q(is_published=True) | Q(author=request.user))
        )
    else:
        recipe = get_object_or_404(
            Recipe,
            id=id,
            is_published=True
        )

    return render(request, 'recipes/recipes_description.html', context={
        'recipe': recipe,
        'is_datail_page': True,
        'page': page
    })

def search(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()

    recipes = (Recipe.objects.filter(
            Q(Q(tittle__icontains = search_term) |
                    Q(description__icontains = search_term)),
            is_published=True,).order_by('-id'))
    page_object, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/search_view.html', context={
        'title': f'q "{search_term}"',
        'search_term': search_term,
        'recipes': page_object,
        'pagination_range':pagination_range,
        'aditional_url_query': f'&q={search_term}',
    })
