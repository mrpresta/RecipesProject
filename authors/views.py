from django.http import Http404
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.


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

def pagina_de_usuario(request):
    return render(request, 'authors/pagina_de_usuario.html')
