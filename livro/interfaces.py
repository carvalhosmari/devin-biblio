from abc import ABC, abstractmethod
from typing import Optional


class ILivroRepository(ABC):
    """Interface para o repositorio de Livro."""

    @abstractmethod
    def criar(self, dados: dict) -> object:
        ...

    @abstractmethod
    def atualizar(self, id_livro: int, dados: dict) -> Optional[object]:
        ...

    @abstractmethod
    def listar_todos(self) -> list:
        ...

    @abstractmethod
    def buscar_por_id(self, id_livro: int) -> Optional[object]:
        ...

    @abstractmethod
    def buscar_por_isbn(self, isbn: str) -> list:
        ...

    @abstractmethod
    def pesquisar(self, filtro: str) -> list:
        ...


class ILivroService(ABC):
    """Interface ILivro conforme especificacao."""

    @abstractmethod
    def cadastrar_livro(self, isbn: str, quantidade: int) -> list:
        ...

    @abstractmethod
    def editar_livro(self, id_livro: int, dados: dict) -> Optional[object]:
        ...

    @abstractmethod
    def listar_livros(self) -> list:
        ...

    @abstractmethod
    def pesquisar_livros(self, filtro: str) -> list:
        ...

    @abstractmethod
    def visualizar_detalhes_livro(self, isbn: str) -> dict:
        ...

    @abstractmethod
    def atualizar_estoque(self, isbn: str, id_livro: int) -> object:
        ...

    @abstractmethod
    def validar_livro(self, isbn: str) -> bool:
        ...

    @abstractmethod
    def buscar_livro_por_id(self, id_livro: int) -> Optional[object]:
        ...
