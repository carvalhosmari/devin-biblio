from django.urls import path

from emprestimo import views

app_name = 'emprestimo'

urlpatterns = [
    path('', views.listar_emprestimos, name='listar'),
    path('registrar/', views.registrar_emprestimo, name='registrar'),
    path('<int:id_emprestimo>/devolver/', views.registrar_devolucao, name='devolver'),
    path('<int:id_emprestimo>/renovar/', views.renovar_emprestimo, name='renovar'),
    path('<int:id_emprestimo>/detalhes/', views.detalhes_emprestimo, name='detalhes'),
]
