from django.contrib import admin

from livro.models import Livro


@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('id', 'isbn', 'titulo', 'autores', 'status')
    list_filter = ('status',)
    search_fields = ('titulo', 'isbn', 'autores')
