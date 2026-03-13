"""
Interface ILeitor
Define o contrato para operacoes relacionadas ao componente Leitor.
"""

from abc import ABC, abstractmethod
from typing import Any


class ILeitor(ABC):
    """Interface para o servico de Leitor."""

    @abstractmethod
    def cadastrar_leitor(self, dados_leitor: dict[str, Any]) -> Any:
        """Cadastra um novo leitor com nome, email, telefone e endereco."""
        ...

    @abstractmethod
    def atualizar_leitor(self, id_leitor: int, dados_leitor: dict[str, Any]) -> Any:
        """Atualiza os dados de um leitor existente."""
        ...

    @abstractmethod
    def listar_leitores(self) -> list[Any]:
        """Lista todos os leitores cadastrados."""
        ...

    @abstractmethod
    def acessar_historico_leitor(self, id_leitor: int) -> Any:
        """Exibe o perfil do leitor e seu historico de emprestimos."""
        ...
