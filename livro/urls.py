from django.urls import path

from livro import views

app_name = 'livro'

urlpatterns = [
    path('', views.listar_livros, name='listar'),
    path('cadastrar/', views.cadastrar_livro, name='cadastrar'),
    path('<int:id_livro>/editar/', views.editar_livro, name='editar'),
    path('isbn/<str:isbn>/detalhes/', views.detalhes_livro, name='detalhes'),
]
