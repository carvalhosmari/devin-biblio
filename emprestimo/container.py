from emprestimo.interfaces import IEmprestimoRepository, IEmprestimoService
from emprestimo.repositories import EmprestimoRepository
from emprestimo.services import IEmprestimo
from leitor.container import LeitorContainer


class EmprestimoContainer:
    """Container de injecao de dependencia para o componente Emprestimo."""

    _repository_instance: IEmprestimoRepository | None = None
    _service_instance: IEmprestimoService | None = None

    @classmethod
    def get_repository(cls) -> IEmprestimoRepository:
        if cls._repository_instance is None:
            cls._repository_instance = EmprestimoRepository()
        return cls._repository_instance

    @classmethod
    def get_service(cls) -> IEmprestimoService:
        if cls._service_instance is None:
            cls._service_instance = IEmprestimo(
                emprestimo_repository=cls.get_repository(),
                leitor_repository=LeitorContainer.get_repository(),
            )
        return cls._service_instance

    @classmethod
    def reset(cls) -> None:
        """Reseta as instancias (util para testes)."""
        cls._repository_instance = None
        cls._service_instance = None
