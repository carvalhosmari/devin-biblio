from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect


urlpatterns = [
    path('admin/', admin.site.urls),
    path('leitor/', include('leitor.urls')),
    path('emprestimo/', include('emprestimo.urls')),
    path('livro/', include('livro.urls')),
    path('', include('index.urls')),
]
