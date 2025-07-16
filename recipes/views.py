from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Recipe
from django.http import Http404

# Create your views here.

def home(request):
    recipes = get_list_or_404(Recipe.objects.order_by('-id'), is_published=True)
    return render(request, 'recipes/home.html', context={
        'recipes': recipes,
    })

def category(request, category_id):
    recipes = get_list_or_404(Recipe.objects.order_by('-id'), category__id=category_id, is_published=True)
    return render(request, 'recipes/category.html', context={
        'recipes': recipes,
        'title': f'{recipes[0].category.name} | Category',
    })

def recipes(request, id):
    recipe = get_object_or_404(Recipe, id=id, is_published=True)
    return render(request, 'recipes/recipes_description.html', context={
        'recipe': recipe,
        'is_datail_page': True,
    })