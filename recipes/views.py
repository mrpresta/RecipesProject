from django.shortcuts import render
from utils.recipes.factory import make_recipe

# Create your views here.

def home(request):
    return render(request, 'recipes/home.html', context={
        'recipes': [make_recipe() for _ in range(10)]
    })

def recipes(request, id):
    return render(request, 'recipes/recipe_description.html', context={
        'recipe': make_recipe,
        'is_datail_page': True,
    })