from django.contrib import admin

from leitor.models import Leitor


@admin.register(Leitor)
class LeitorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email', 'telefone', 'ativo', 'data_cadastro')
    list_filter = ('ativo',)
    search_fields = ('nome', 'email')
