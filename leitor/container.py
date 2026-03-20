from leitor.interfaces import ILeitorRepository, ILeitorService
from leitor.repositories import LeitorRepository
from leitor.services import ILeitor


class LeitorContainer:
    """Container de injecao de dependencia para o componente Leitor."""

    _repository_instance: ILeitorRepository | None = None
    _service_instance: ILeitorService | None = None

    @classmethod
    def get_repository(cls) -> ILeitorRepository:
        if cls._repository_instance is None:
            cls._repository_instance = LeitorRepository()
        return cls._repository_instance

    @classmethod
    def get_service(cls) -> ILeitorService:
        if cls._service_instance is None:
            cls._service_instance = ILeitor(
                repository=cls.get_repository()
            )
        return cls._service_instance

    @classmethod
    def reset(cls) -> None:
        """Reseta as instancias (util para testes)."""
        cls._repository_instance = None
        cls._service_instance = None
