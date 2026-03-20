from django.urls import path

from leitor import views

app_name = 'leitor'

urlpatterns = [
    path('', views.listar_leitores, name='listar'),
    path('cadastrar/', views.cadastrar_leitor, name='cadastrar'),
    path('<int:id_leitor>/editar/', views.editar_leitor, name='editar'),
    path('<int:id_leitor>/perfil/', views.perfil_leitor, name='perfil'),
]
