from livro.interfaces import ILivroRepository, ILivroService
from livro.repositories import LivroRepository
from livro.services import ILivro


class LivroContainer:
    """Container de injecao de dependencia para o componente Livro."""

    _repository_instance: ILivroRepository | None = None
    _service_instance: ILivroService | None = None

    @classmethod
    def get_repository(cls) -> ILivroRepository:
        if cls._repository_instance is None:
            cls._repository_instance = LivroRepository()
        return cls._repository_instance

    @classmethod
    def get_service(cls) -> ILivroService:
        if cls._service_instance is None:
            cls._service_instance = ILivro(
                repository=cls.get_repository()
            )
        return cls._service_instance

    @classmethod
    def reset(cls) -> None:
        """Reseta as instancias (util para testes)."""
        cls._repository_instance = None
        cls._service_instance = None
