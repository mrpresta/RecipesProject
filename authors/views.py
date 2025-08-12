from django.http import Http404
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib import messages
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

    return redirect('authors:register')


def login(request):
    if request.POST:
        form = LoginForm(request.POST)
    else:
        form = LoginForm()
    return render(request,'authors/login.html', {
        'form': form,
    })