from typing import Optional

from django.utils import timezone

from emprestimo.interfaces import IEmprestimoRepository
from emprestimo.models import Emprestimo


class EmprestimoRepository(IEmprestimoRepository):
    """Implementacao concreta do repositorio de Emprestimo usando Django ORM."""

    def criar(self, dados: dict) -> Emprestimo:
        emprestimo = Emprestimo(**dados)
        emprestimo.save()
        return emprestimo

    def atualizar(self, id_emprestimo: int, dados: dict) -> Optional[Emprestimo]:
        try:
            emprestimo = Emprestimo.objects.get(pk=id_emprestimo)
        except Emprestimo.DoesNotExist:
            return None
        for campo, valor in dados.items():
            setattr(emprestimo, campo, valor)
        emprestimo.save()
        return emprestimo

    def buscar_por_id(self, id_emprestimo: int) -> Optional[Emprestimo]:
        try:
            return Emprestimo.objects.select_related('id_leitor', 'id_livro').get(
                pk=id_emprestimo
            )
        except Emprestimo.DoesNotExist:
            return None

    def listar_ativos(self, id_leitor: int | None = None) -> list[Emprestimo]:
        qs = Emprestimo.objects.select_related('id_leitor', 'id_livro').filter(
            status__in=['ativo', 'atrasado', 'renovado', 'devolvido']
        )
        if id_leitor is not None:
            qs = qs.filter(id_leitor_id=id_leitor)
        return list(qs)

    def listar_por_leitor(self, id_leitor: int) -> list[Emprestimo]:
        return list(
            Emprestimo.objects.select_related('id_leitor', 'id_livro')
            .filter(id_leitor_id=id_leitor)
            .order_by('-data_emprestimo')
        )

    def buscar_pendencias_leitor(self, id_leitor: int) -> list[Emprestimo]:
        agora = timezone.now()
        pendencias = Emprestimo.objects.filter(
            id_leitor_id=id_leitor,
            status__in=['ativo', 'atrasado', 'renovado'],
            data_limite__lt=agora,
        )
        # Atualizar status para atrasado se necessario
        for emp in pendencias:
            if emp.status != 'atrasado':
                emp.status = 'atrasado'
                emp.save()
        return list(
            Emprestimo.objects.filter(
                id_leitor_id=id_leitor,
                status='atrasado',
                data_devolucao__isnull=True,
            )
        )
