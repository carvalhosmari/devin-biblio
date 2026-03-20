import os
import re
from typing import Optional

import requests

from livro.interfaces import ILivroRepository, ILivroService
from livro.models import Livro


GOOGLE_BOOKS_API_KEY = os.environ.get('GOOGLE_BOOKS_API_KEY', '')
GOOGLE_BOOKS_API_URL = 'https://www.googleapis.com/books/v1/volumes'


class ILivro(ILivroService):
    """Implementacao concreta do servico de Livro com injecao de dependencia."""

    def __init__(self, repository: ILivroRepository):
        self._repository = repository

    def cadastrar_livro(self, isbn: str, quantidade: int = 1) -> list[Livro]:
        """
        Cadastra livro(s) a partir do ISBN.
        Busca informacoes na API Google Books.
        O usuario informa a quantidade de exemplares a cadastrar.
        """
        isbn_limpo = self._limpar_isbn(isbn)
        if not self.validar_livro(isbn_limpo):
            raise ValueError(f"ISBN '{isbn}' nao e valido.")

        dados_api = self._buscar_google_books(isbn_limpo)

        livros_criados = []
        for _ in range(quantidade):
            livro = self._repository.criar({
                'isbn': isbn_limpo,
                'titulo': dados_api.get('titulo', 'Titulo nao encontrado'),
                'autores': dados_api.get('autores', 'Autor desconhecido'),
                'pais': dados_api.get('pais', ''),
                'editora': dados_api.get('editora', ''),
                'edicao': dados_api.get('edicao', ''),
                'status': 'disponivel',
            })
            livros_criados.append(livro)
            print(f"Livro cadastrado: {livro})")
        
        return livros_criados

    def editar_livro(self, id_livro: int, dados: dict) -> Optional[Livro]:
        """Edita as informacoes de um determinado livro."""
        livro = self._repository.buscar_por_id(id_livro)
        if not livro:
            raise ValueError(f"Livro com ID {id_livro} nao encontrado.")
        return self._repository.atualizar(id_livro, dados)

    def listar_livros(self) -> list[Livro]:
        """Lista todos os livros."""
        return self._repository.listar_todos()

    def pesquisar_livros(self, filtro: str) -> list[Livro]:
        """Pesquisar livros com base nas informacoes (titulo, autor, editora, etc)."""
        if not filtro or not filtro.strip():
            return self._repository.listar_todos()
        return self._repository.pesquisar(filtro.strip())

    def visualizar_detalhes_livro(self, isbn: str) -> dict:
        """Visualizar informacoes de livros a partir do ISBN."""
        isbn_limpo = self._limpar_isbn(isbn)
        exemplares = self._repository.buscar_por_isbn(isbn_limpo)
        if not exemplares:
            raise ValueError(f"Nenhum livro encontrado com ISBN '{isbn}'.")

        primeiro = exemplares[0]
        total = len(exemplares)
        disponiveis = sum(1 for e in exemplares if e.status == 'disponivel')
        emprestados = total - disponiveis

        return {
            'isbn': isbn_limpo,
            'titulo': primeiro.titulo,
            'autores': primeiro.autores,
            'pais': primeiro.pais,
            'editora': primeiro.editora,
            'edicao': primeiro.edicao,
            'total_exemplares': total,
            'disponiveis': disponiveis,
            'emprestados': emprestados,
            'exemplares': exemplares,
        }

    def atualizar_estoque(self, isbn: str, id_livro: int) -> Livro:
        """Atualiza status do livro: disponivel <-> emprestado."""
        livro = self._repository.buscar_por_id(id_livro)
        if not livro:
            raise ValueError(f"Livro com ID {id_livro} nao encontrado.")

        novo_status = 'emprestado' if livro.status == 'disponivel' else 'disponivel'
        return self._repository.atualizar(id_livro, {'status': novo_status})

    def validar_livro(self, isbn: str) -> bool:
        """Valida se o ISBN informado e valido (ISBN-10 ou ISBN-13)."""
        isbn_limpo = self._limpar_isbn(isbn)
        if len(isbn_limpo) == 10:
            return self._validar_isbn10(isbn_limpo)
        elif len(isbn_limpo) == 13:
            return self._validar_isbn13(isbn_limpo)
        return False

    def buscar_livro_por_id(self, id_livro: int) -> Optional[Livro]:
        """Busca um livro pelo ID."""
        return self._repository.buscar_por_id(id_livro)

    def _buscar_google_books(self, isbn: str) -> dict:
        """Busca informacoes do livro na API Google Books."""
        try:
            params = {'q': f'isbn:{isbn}'}
            if GOOGLE_BOOKS_API_KEY:
                params['key'] = GOOGLE_BOOKS_API_KEY

            response = requests.get(GOOGLE_BOOKS_API_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get('totalItems', 0) == 0:
                return {'titulo': isbn, 'autores': 'Desconhecido'}

            volume = data['items'][0]['volumeInfo']
            access_info = data['items'][0].get('accessInfo', {})
            return {
                'titulo': volume.get('title', 'Titulo nao encontrado'),
                'autores': ', '.join(volume.get('authors', ['Autor desconhecido'])),
                'pais': access_info.get('country', ''),
                'editora': volume.get('publisher', ''),
                'edicao': volume.get('edition', ''),
            }
        except requests.RequestException:
            return {'titulo': isbn, 'autores': 'Informacao indisponivel (erro na API)'}

    @staticmethod
    def _limpar_isbn(isbn: str) -> str:
        """Remove hifens e espacos do ISBN."""
        return re.sub(r'[-\s]', '', isbn.strip())

    @staticmethod
    def _validar_isbn10(isbn: str) -> bool:
        """Valida ISBN-10."""
        if not re.match(r'^\d{9}[\dXx]$', isbn):
            return False
        total = sum(
            (10 if c in ('X', 'x') else int(c)) * (10 - i)
            for i, c in enumerate(isbn)
        )
        return total % 11 == 0

    @staticmethod
    def _validar_isbn13(isbn: str) -> bool:
        """Valida ISBN-13."""
        if not isbn.isdigit():
            return False
        total = sum(
            int(c) * (1 if i % 2 == 0 else 3)
            for i, c in enumerate(isbn)
        )
        return total % 10 == 0
