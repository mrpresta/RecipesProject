from django.urls import path
from . import views

app_name = 'authors'

urlpatterns = [
    path('cadastro/', views.register, name='register'),
    path('cadastro/create/', views.register_create, name='create'),
    path('login/', views.login_view, name='login'),
    path('login/create/', views.login_create, name='login_create'),
    path('login/create/pagina_de_usuario/', views.pagina_de_usuario, name='pagina_de_usuario'),
    path('login/create/pagina_de_usuario/logout', views.logout_view, name='logout')

]