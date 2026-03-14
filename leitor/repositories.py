from typing import Optional

from leitor.interfaces import ILeitorRepository
from leitor.models import Leitor


class LeitorRepository(ILeitorRepository):
    """Implementacao concreta do repositorio de Leitor usando Django ORM."""

    def criar(self, dados: dict) -> Leitor:
        leitor = Leitor(**dados)
        leitor.save()
        return leitor

    def atualizar(self, id_leitor: int, dados: dict) -> Optional[Leitor]:
        try:
            leitor = Leitor.objects.get(pk=id_leitor)
        except Leitor.DoesNotExist:
            return None
        for campo, valor in dados.items():
            setattr(leitor, campo, valor)
        leitor.save()
        return leitor

    def listar_todos(self) -> list[Leitor]:
        return list(Leitor.objects.all())

    def buscar_por_id(self, id_leitor: int) -> Optional[Leitor]:
        try:
            return Leitor.objects.get(pk=id_leitor)
        except Leitor.DoesNotExist:
            return None

    def buscar_por_cpf(self, cpf: str) -> Optional[Leitor]:
        try:
            return Leitor.objects.get(cpf=cpf)
        except Leitor.DoesNotExist:
            return None
