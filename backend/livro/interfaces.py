"""
Interface ILivro
Define o contrato para operacoes relacionadas ao componente Livro.
"""

from abc import ABC, abstractmethod
from typing import Any


class ILivro(ABC):
    """Interface para o servico de Livro."""

    @abstractmethod
    def cadastrar_livro(self, isbn: str, quantidade: int) -> Any:
        """Cadastra um novo livro a partir do ISBN."""
        ...

    @abstractmethod
    def editar_livro(self, id_livro: int, isbn: str, dados_livro: dict[str, Any]) -> Any:
        """Edita as informacoes de um determinado livro."""
        ...

    @abstractmethod
    def listar_livros(self) -> list[Any]:
        """Lista todos os livros agrupados por ISBN."""
        ...

    @abstractmethod
    def pesquisar_livros(self, filtro: str) -> list[Any]:
        """Pesquisar livros com base nas informacoes (titulo, autor, editora, etc)."""
        ...

    @abstractmethod
    def visualizar_detalhes_livro(self, isbn: str) -> Any:
        """Visualizar as informacoes de um determinado livro a partir do ISBN."""
        ...

    @abstractmethod
    def atualizar_estoque(self, isbn: str, id_livro: int) -> Any:
        """Atualiza quantidade disponivel, alterando o status disponivel <-> emprestado."""
        ...

    @abstractmethod
    def validar_livro(self, isbn: str) -> bool:
        """Valida se o ISBN informado e valido."""
        ...
