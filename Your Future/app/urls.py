from django.urls import path 
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
    path('cadastro/', views.cadastrar_user, name='cadastrar_user'),
    path('contato/', views.contato, name='contato'),
    path('pagamento/', views.pagamento, name='pagamento'),
    path('usuarios/', views.exibir_user, name='exibir_user'),
    path('cadastrarcurso/', views.cadastrar_curso, name='cadastrar_curso'),
    path('cursos/', views.exibir_curso, name='exibir_curso'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.fazer_login, name='login'), 
    path('logout/', views.logout, name='logout'),
    path('redefinir_senha/', views.redefinir_senha, name='redefinir_senha'),

    #FOTO
    path('add-foto', views.add_foto, name = 'add_foto'),
    path('galeria/', views.galeria, name = 'galeria'),

    #EDITAR E EXCLUIR
    path('editar_usuario/<int:id_usuario>', views.editar_usuario, name = 'editar_usuario'),
    path('excluir_usuario/<int:id_usuario>', views.excluir_usuario, name = 'excluir_usuario'),

    #VENDA
    path('comprar/<int:curso_id>/', views.comprar_curso, name='comprar_curso'),
    path('relatorio-vendas/', views.relatorio_vendas, name='relatorio_vendas'),
]