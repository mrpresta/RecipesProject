from django.http import Http404
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm, CadastrarReceitaForm
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from utils.pagination import make_pagination
from recipes.models import Recipe
from django.utils.text import slugify
from django.shortcuts import get_object_or_404

import os
# Create your views here.


PER_PAGE = os.environ.get('PER_PAGE', 3)

def register(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)

    return render(request,'authors/register.html', {
        'form': form,
    })

def register_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, 'Você foi cadastrado com sucesso')

        del(request.session['register_form_data'])
        return redirect(reverse('authors:login'))
    return redirect('authors:register')


def login_view(request):
    if request.user.is_authenticated:
        logout(request)

    form = LoginForm()

    return render(request,'authors/login.html', {
        'form': form,
        'form_action': reverse('authors:login_create')
    })

def login_create(request):
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)
    login_url = reverse('authors:login')

    if form.is_valid():
        authenticated_user = authenticate(request,
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            login(request, authenticated_user)
            return redirect('authors:pagina_de_usuario')
        else:
            messages.error(request,'Usuario ou senha incorretos')
    else:
        messages.error(request, 'Usuario ou senha incorretos')

    return redirect(login_url)

@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        messages.error(request, 'Invalid request')
        return redirect(reverse('authors:login'))

    if request.POST.get('username') != request.user.username:
        messages.error(request, 'Divergent User')
        return redirect(reverse('authors:login'))

    logout(request)
    messages.success(request, 'Logout User')
    return redirect(reverse('authors:login'))

@login_required(login_url='authors:login', redirect_field_name='next')
def pagina_de_usuario(request):
    return render(request, 'authors/pagina_de_usuario.html')


@login_required(login_url='authors:login', redirect_field_name='next')
def cadastrar_receita(request):
    if request.method == "POST":
        form = CadastrarReceitaForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.is_published = False

            if not recipe.id:
                base_slug = slugify(recipe.tittle)
                slug = base_slug
                counter = 1
                while Recipe.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                recipe.slug = slug

            recipe.save()
            messages.success(request,'recipe cadastrada com sucesso')

            return redirect('authors:pagina_de_usuario')
        else:
            messages.error('Receita nao cadastrada. Verifique os campos e tente novamente')
    else:
        form = CadastrarReceitaForm()

    return render(request, 'authors/cadastrar_receita.html', context={'form':form})


@login_required(login_url='authors:login', redirect_field_name='next')
def receitas_publicadas(request):
    recipes = Recipe.objects.filter(author=request.user, is_published=True)
    page_object, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'authors/receitas_publicadas.html',
    context = {
        'recipes': page_object,
        'pagination_range': pagination_range,
    })

@login_required(login_url='authors:login', redirect_field_name='next')
def receitas_em_revisao(request):
    recipes = Recipe.objects.filter(author=request.user, is_published=False)
    page_object, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'authors/receitas_em_revisao.html',
    context = {
        'recipes': page_object,
        'pagination_range': pagination_range,
        'from_painel_de_usuario': True
    })

@login_required(login_url='authors:login')
def apagar_receita(request, id):
    recipe = get_object_or_404(Recipe, id=id, author=request.user)

    if request.method == "POST":
        recipe.delete()
        messages.success(request, "Receita apagada com sucesso!")
        return redirect('authors:pagina_de_usuario')
    else:
        messages.error(request, "Ação inválida.")
        return redirect('authors:pagina_de_usuario')

@login_required(login_url='authors:login')
def editar_receita(request, id):
    recipe = get_object_or_404(Recipe, id=id)

    if request.method == 'POST':
        form = CadastrarReceitaForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request, 'Receita editada com sucesso')
            return redirect('authors:pagina_de_usuario')
        else:
            messages.error(request, 'algo deu errao verifique e tente novamente')
            form = CadastrarReceitaForm(instance=recipe)

    else:
        form = CadastrarReceitaForm(instance=recipe)
    return render(request,'authors/editar_receita.html', {'form':form, 'recipe':recipe})