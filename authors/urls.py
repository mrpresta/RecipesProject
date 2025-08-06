from django.urls import path
from . import views

app_name = 'authors'

urlpatterns = [
    path('cadastro/', views.register, name='register'),
    path('cadastro/create/', views.register_create, name='create'),
    path('login/', views.login, name='login'),
]