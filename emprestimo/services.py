from datetime import timedelta
from decimal import Decimal
from typing import Optional

from django.utils import timezone

from emprestimo.interfaces import IEmprestimoRepository, IEmprestimoService
from emprestimo.models import Emprestimo
from leitor.interfaces import ILeitorRepository
from livro.models import Livro

PRAZO_EMPRESTIMO_DIAS = 7
MAX_RENOVACOES = 2
MULTA_POR_DIA = Decimal('1.00')


class IEmprestimo(IEmprestimoService):
    """Implementacao concreta do servico de Emprestimo com injecao de dependencia."""

    def __init__(
        self,
        emprestimo_repository: IEmprestimoRepository,
        leitor_repository: ILeitorRepository,
    ):
        self._emprestimo_repo = emprestimo_repository
        self._leitor_repo = leitor_repository

    def registrar_emprestimo(self, id_leitor: int, id_livro: int) -> Emprestimo:
        """
        Registra um novo emprestimo.
        Regras:
        - Leitor deve estar ativo
        - Livro deve estar disponivel
        - Leitor nao pode ter pendencias de devolucao
        """
        leitor = self.validar_leitor(id_leitor)

        try:
            livro = Livro.objects.get(pk=id_livro)
        except Livro.DoesNotExist:
            raise ValueError(f"Livro com ID {id_livro} nao encontrado.")

        if livro.status != 'disponivel':
            raise ValueError(f"Livro '{livro.titulo}' nao esta disponivel para emprestimo.")

        pendencias = self._emprestimo_repo.buscar_pendencias_leitor(id_leitor)
        if pendencias:
            raise ValueError(
                f"Leitor '{leitor.nome}' possui {len(pendencias)} emprestimo(s) atrasado(s). "
                "Regularize as pendencias antes de realizar um novo emprestimo."
            )

        agora = timezone.now()
        data_limite = agora + timedelta(days=PRAZO_EMPRESTIMO_DIAS)

        emprestimo = self._emprestimo_repo.criar({
            'id_leitor': leitor,
            'id_livro': livro,
            'data_limite': data_limite,
            'status': 'ativo',
        })

        livro.status = 'emprestado'
        livro.save()

        return emprestimo

    def registrar_devolucao(self, id_emprestimo: int) -> Emprestimo:
        """
        Registra a devolucao de um livro.
        Calcula multa em caso de atraso (R$1,00 por dia).
        """
        emprestimo = self._emprestimo_repo.buscar_por_id(id_emprestimo)
        if not emprestimo:
            raise ValueError(f"Emprestimo com ID {id_emprestimo} nao encontrado.")

        if emprestimo.status == 'devolvido':
            raise ValueError("Este emprestimo ja foi devolvido.")

        agora = timezone.now()
        multa = self._calcular_multa(emprestimo, agora)

        emprestimo = self._emprestimo_repo.atualizar(id_emprestimo, {
            'data_devolucao': agora,
            'status': 'devolvido',
        })

        livro = emprestimo.id_livro
        livro.status = 'disponivel'
        livro.save()

        resultado = {
            'emprestimo': emprestimo,
            'multa': multa,
        }
        return resultado

    def renovar_emprestimo(self, id_emprestimo: int) -> Emprestimo:
        """
        Renova o emprestimo por mais 14 dias (maximo 2 renovacoes).
        Encerra o emprestimo atual e cria um novo com novas datas.
        """
        emprestimo = self._emprestimo_repo.buscar_por_id(id_emprestimo)
        if not emprestimo:
            raise ValueError(f"Emprestimo com ID {id_emprestimo} nao encontrado.")

        if emprestimo.status == 'devolvido':
            raise ValueError("Nao e possivel renovar um emprestimo ja devolvido.")

        if emprestimo.renovacoes >= MAX_RENOVACOES:
            raise ValueError(
                f"Maximo de {MAX_RENOVACOES} renovacoes atingido para este emprestimo."
            )

        self._emprestimo_repo.atualizar(id_emprestimo, {
            'status': 'renovado',
        })

        agora = timezone.now()
        data_limite = agora + timedelta(days=PRAZO_EMPRESTIMO_DIAS * 2)

        novo_emprestimo = self._emprestimo_repo.criar({
            'id_leitor': emprestimo.id_leitor,
            'id_livro': emprestimo.id_livro,
            'data_limite': data_limite,
            'status': 'ativo',
            'renovacoes': emprestimo.renovacoes + 1,
        })

        return novo_emprestimo

    def visualizar_emprestimos_ativos(
        self, id_leitor: int | None = None
    ) -> list[Emprestimo]:
        """Lista emprestimos ativos, opcionalmente filtrados por leitor."""
        emprestimos = self._emprestimo_repo.listar_ativos(id_leitor)
        agora = timezone.now()
        for emp in emprestimos:
            if emp.status == 'ativo' and emp.data_limite < agora:
                emp.status = 'atrasado'
                emp.save()
        return emprestimos

    def validar_leitor(self, id_leitor: int) -> object:
        """Valida se o leitor existe e esta ativo."""
        leitor = self._leitor_repo.buscar_por_id(id_leitor)
        if not leitor:
            raise ValueError(f"Leitor com ID {id_leitor} nao encontrado.")
        if not leitor.ativo:
            raise ValueError(f"Leitor '{leitor.nome}' esta inativo.")
        return leitor

    def validar_prazo(self, id_emprestimo: int) -> dict:
        """Verifica o status do prazo do emprestimo."""
        emprestimo = self._emprestimo_repo.buscar_por_id(id_emprestimo)
        if not emprestimo:
            raise ValueError(f"Emprestimo com ID {id_emprestimo} nao encontrado.")

        agora = timezone.now()
        multa = self._calcular_multa(emprestimo, agora)
        dias_restantes = (emprestimo.data_limite - agora).days

        return {
            'emprestimo': emprestimo,
            'atrasado': dias_restantes < 0,
            'dias_restantes': max(dias_restantes, 0),
            'dias_atraso': abs(min(dias_restantes, 0)),
            'multa': multa,
        }

    def buscar_emprestimos_leitor(self, id_leitor: int) -> list[Emprestimo]:
        """Busca todos os emprestimos de um leitor (para historico)."""
        return self._emprestimo_repo.listar_por_leitor(id_leitor)

    @staticmethod
    def _calcular_multa(emprestimo: Emprestimo, data_referencia) -> Decimal:
        """Calcula multa por atraso (R$1,00 por dia)."""
        if data_referencia > emprestimo.data_limite:
            dias_atraso = (data_referencia - emprestimo.data_limite).days
            return MULTA_POR_DIA * dias_atraso
        return Decimal('0.00')
