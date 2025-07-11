from django.shortcuts import render, get_object_or_404
from .models import Recipe

# Create your views here.

def home(request):
    recipes = Recipe.objects.all().order_by('-id')
    return render(request, 'recipes/home.html', context={
        'recipes': recipes,
    })

def category(request, category_id):
    recipes = Recipe.objects.filter(category__id=category_id).order_by('-id')
    return render(request, 'recipes/home.html', context={
        'recipes': recipes,
    })

def recipes(request, id):
    recipes = get_object_or_404(Recipe, id=id)
    return render(request, 'recipes/recipes_description.html', context={
        'recipe': recipes,
        'is_datail_page': True,
    })