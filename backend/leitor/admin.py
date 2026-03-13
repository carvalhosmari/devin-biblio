"""
Admin: Leitor
Configuracao do Django Admin para o componente Leitor.
"""

from django.contrib import admin

from .models import Leitor

admin.site.register(Leitor)
