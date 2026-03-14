from abc import ABC, abstractmethod
from typing import Optional


class ILeitorRepository(ABC):
    """Interface para o repositorio de Leitor (camada de acesso a dados)."""

    @abstractmethod
    def criar(self, dados: dict) -> object:
        """Cria um novo leitor no banco de dados."""
        ...

    @abstractmethod
    def atualizar(self, id_leitor: int, dados: dict) -> Optional[object]:
        """Atualiza um leitor existente."""
        ...

    @abstractmethod
    def listar_todos(self) -> list:
        """Lista todos os leitores."""
        ...

    @abstractmethod
    def buscar_por_id(self, id_leitor: int) -> Optional[object]:
        """Busca um leitor pelo ID."""
        ...

    @abstractmethod
    def buscar_por_cpf(self, cpf: str) -> Optional[object]:
        """Busca um leitor pelo CPF."""
        ...


class ILeitorService(ABC):
    """Interface ILeitor conforme especificacao."""

    @abstractmethod
    def cadastrar_leitor(self, dados_leitor: dict) -> object:
        """Cadastra um novo leitor com nome, email, telefone e endereco."""
        ...

    @abstractmethod
    def atualizar_leitor(self, id_leitor: int, dados_leitor: dict) -> Optional[object]:
        """Atualiza os dados de um leitor existente."""
        ...

    @abstractmethod
    def listar_leitores(self) -> list:
        """Lista todos os leitores cadastrados."""
        ...

    @abstractmethod
    def acessar_historico_leitor(self, id_leitor: int) -> Optional[dict]:
        """Exibe o perfil do leitor e seu historico de emprestimos."""
        ...
