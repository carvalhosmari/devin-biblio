"""
Interface IEmprestimo
Define o contrato para operacoes relacionadas ao componente Emprestimo.
"""

from abc import ABC, abstractmethod
from typing import Any


class IEmprestimo(ABC):
    """Interface para o servico de Emprestimo."""

    @abstractmethod
    def registrar_emprestimo(self, id_leitor: int, id_livro: int) -> Any:
        """Registra um novo emprestimo."""
        ...

    @abstractmethod
    def registrar_devolucao(self, id_emprestimo: int) -> Any:
        """Registra a devolucao de um livro e atualiza o estoque."""
        ...

    @abstractmethod
    def renovar_emprestimo(self, id_emprestimo: int) -> Any:
        """Renova o emprestimo por mais 14 dias (maximo 2 renovacoes)."""
        ...

    @abstractmethod
    def visualizar_emprestimos_ativos(self, id_leitor: int | None = None) -> list[Any]:
        """Lista emprestimos ativos, opcionalmente filtrados por leitor."""
        ...

    @abstractmethod
    def validar_leitor(self, id_leitor: int) -> bool:
        """Valida se o leitor existe e esta ativo."""
        ...

    @abstractmethod
    def validar_prazo(self, id_emprestimo: int) -> Any:
        """Verifica o status do prazo do emprestimo."""
        ...
