from typing import Optional

from django.db.models import Q

from livro.interfaces import ILivroRepository
from livro.models import Livro


class LivroRepository(ILivroRepository):
    """Implementacao concreta do repositorio de Livro usando Django ORM."""

    def criar(self, dados: dict) -> Livro:
        livro = Livro(**dados)
        livro.save()
        return livro

    def atualizar(self, id_livro: int, dados: dict) -> Optional[Livro]:
        try:
            livro = Livro.objects.get(pk=id_livro)
        except Livro.DoesNotExist:
            return None
        for campo, valor in dados.items():
            setattr(livro, campo, valor)
        livro.save()
        return livro

    def listar_todos(self) -> list[Livro]:
        return list(Livro.objects.all())

    def buscar_por_id(self, id_livro: int) -> Optional[Livro]:
        try:
            return Livro.objects.get(pk=id_livro)
        except Livro.DoesNotExist:
            return None

    def buscar_por_isbn(self, isbn: str) -> list[Livro]:
        return list(Livro.objects.filter(isbn=isbn))

    def pesquisar(self, filtro: str) -> list[Livro]:
        return list(
            Livro.objects.filter(
                Q(titulo__icontains=filtro)
                | Q(autores__icontains=filtro)
                | Q(editora__icontains=filtro)
                | Q(isbn__icontains=filtro)
            )
        )
