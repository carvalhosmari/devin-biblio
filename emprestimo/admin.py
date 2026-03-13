from django.contrib import admin

from emprestimo.models import Emprestimo


@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'id_leitor', 'id_livro', 'data_emprestimo',
        'data_limite', 'data_devolucao', 'status', 'renovacoes',
    )
    list_filter = ('status',)
    search_fields = ('id_leitor__nome', 'id_livro__titulo')
