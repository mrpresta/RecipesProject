from django.urls import path
from . import views

app_name = 'authors'

urlpatterns = [
    path('cadastro/', views.register, name='register'),
    path('cadastro/create/', views.register_create, name='create'),
    path('login/', views.login_view, name='login'),
    path('login/create/', views.login_create, name='login_create'),
    path('pagina_de_usuario/', views.pagina_de_usuario, name='pagina_de_usuario'),
    path('pagina_de_usuario/logout', views.logout_view, name='logout'),
    path('receitas_publicadas/', views.receitas_publicadas, name='receitas_publicadas'),
    path('receitas_em_revisao/', views.receitas_em_revisao, name='receitas_em_revisao'),
    path('receitas_em_revisao/editar_receita/<int:id>/', views.editar_receita, name='editar_receita'),
    path('cadastrar_receita/', views.cadastrar_receita, name='cadastrar_receitas'),
    path('apagar_receita/<int:id>/', views.apagar_receita, name='apagar_receita'),
]