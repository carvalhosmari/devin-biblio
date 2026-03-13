"""
Admin: Emprestimo
Configuracao do Django Admin para o componente Emprestimo.
"""

from django.contrib import admin

from .models import Emprestimo

admin.site.register(Emprestimo)
