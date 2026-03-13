"""
Admin: Livro
Configuracao do Django Admin para o componente Livro.
"""

from django.contrib import admin

from .models import Livro

admin.site.register(Livro)
