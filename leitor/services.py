from typing import Optional

from leitor.interfaces import ILeitorRepository, ILeitorService
from leitor.models import Leitor


class LeitorService(ILeitorService):
    """Implementacao concreta do servico de Leitor com injecao de dependencia."""

    def __init__(self, repository: ILeitorRepository):
        self._repository = repository

    def cadastrar_leitor(self, dados_leitor: dict) -> Leitor:
        """
        Cadastra um novo leitor.
        Regra: O cadastro so ocorre se nao houver leitor com o mesmo email.
        """
        email = dados_leitor.get('email', '')
        leitor_existente = self._repository.buscar_por_email(email)
        if leitor_existente:
            raise ValueError(f"Ja existe um leitor cadastrado com o email: {email}")

        dados_leitor.setdefault('ativo', True)
        return self._repository.criar(dados_leitor)

    def atualizar_leitor(self, id_leitor: int, dados_leitor: dict) -> Optional[Leitor]:
        """Atualiza os dados de um leitor existente."""
        leitor = self._repository.buscar_por_id(id_leitor)
        if not leitor:
            raise ValueError(f"Leitor com ID {id_leitor} nao encontrado.")

        if 'email' in dados_leitor and dados_leitor['email'] != leitor.email:
            existente = self._repository.buscar_por_email(dados_leitor['email'])
            if existente:
                raise ValueError(
                    f"Ja existe um leitor cadastrado com o email: {dados_leitor['email']}"
                )

        return self._repository.atualizar(id_leitor, dados_leitor)

    def listar_leitores(self) -> list[Leitor]:
        """Lista todos os leitores cadastrados."""
        return self._repository.listar_todos()

    def acessar_historico_leitor(self, id_leitor: int) -> Optional[dict]:
        """
        Exibe o perfil do leitor e seu historico de emprestimos.
        O historico de emprestimos sera implementado no componente Emprestimo.
        """
        leitor = self._repository.buscar_por_id(id_leitor)
        if not leitor:
            raise ValueError(f"Leitor com ID {id_leitor} nao encontrado.")

        return {
            'leitor': leitor,
            'emprestimos': [],  # Sera preenchido pelo componente Emprestimo
        }
