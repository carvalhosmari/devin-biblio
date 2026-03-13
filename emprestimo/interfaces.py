from abc import ABC, abstractmethod
from typing import Optional


class IEmprestimoRepository(ABC):
    """Interface para o repositorio de Emprestimo."""

    @abstractmethod
    def criar(self, dados: dict) -> object:
        ...

    @abstractmethod
    def atualizar(self, id_emprestimo: int, dados: dict) -> Optional[object]:
        ...

    @abstractmethod
    def buscar_por_id(self, id_emprestimo: int) -> Optional[object]:
        ...

    @abstractmethod
    def listar_ativos(self, id_leitor: int | None = None) -> list:
        ...

    @abstractmethod
    def listar_por_leitor(self, id_leitor: int) -> list:
        ...

    @abstractmethod
    def buscar_pendencias_leitor(self, id_leitor: int) -> list:
        ...


class IEmprestimoService(ABC):
    """Interface IEmprestimo conforme especificacao."""

    @abstractmethod
    def registrar_emprestimo(self, id_leitor: int, id_livro: int) -> object:
        ...

    @abstractmethod
    def registrar_devolucao(self, id_emprestimo: int) -> object:
        ...

    @abstractmethod
    def renovar_emprestimo(self, id_emprestimo: int) -> object:
        ...

    @abstractmethod
    def visualizar_emprestimos_ativos(self, id_leitor: int | None = None) -> list:
        ...

    @abstractmethod
    def validar_leitor(self, id_leitor: int) -> object:
        ...

    @abstractmethod
    def validar_prazo(self, id_emprestimo: int) -> dict:
        ...
