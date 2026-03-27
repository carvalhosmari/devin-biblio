import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bibliomania.settings')
django.setup()

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from livro.container import LivroContainer

api = FastAPI(title="Bibliomania Livro API", version="1.0.0")


class LivroCadastrarSchema(BaseModel):
    isbn: str
    quantidade: int = 1


class LivroUpdateSchema(BaseModel):
    isbn: str | None = None
    titulo: str | None = None
    autores: str | None = None
    pais: str | None = None
    editora: str | None = None
    edicao: str | None = None


class LivroResponseSchema(BaseModel):
    id: int
    isbn: str
    titulo: str
    autores: str
    pais: str | None = None
    editora: str | None = None
    edicao: str | None = None
    status: str

    class Config:
        from_attributes = True


def _livro_to_dict(livro) -> dict:
    return {
        'id': livro.id,
        'isbn': livro.isbn,
        'titulo': livro.titulo,
        'autores': livro.autores,
        'pais': livro.pais,
        'editora': livro.editora,
        'edicao': livro.edicao,
        'status': livro.status,
    }


@api.get("/api/livros", response_model=list[LivroResponseSchema])
def listar_livros(filtro: str | None = Query(None)):
    """Lista todos os livros, com pesquisa opcional."""
    service = LivroContainer.get_service()
    if filtro:
        livros = service.pesquisar_livros(filtro)
    else:
        livros = service.listar_livros()
    return [_livro_to_dict(l) for l in livros]


@api.post("/api/livros", response_model=list[LivroResponseSchema], status_code=201)
def cadastrar_livro(dados: LivroCadastrarSchema):
    """Cadastra livro(s) a partir do ISBN via Google Books API."""
    service = LivroContainer.get_service()
    try:
        livros = service.cadastrar_livro(dados.isbn, dados.quantidade)
        return [_livro_to_dict(l) for l in livros]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@api.put("/api/livros/{id_livro}", response_model=LivroResponseSchema)
def editar_livro(id_livro: int, dados: LivroUpdateSchema):
    """Edita as informacoes de um livro."""
    service = LivroContainer.get_service()
    try:
        dados_filtrados = {k: v for k, v in dados.model_dump().items() if v is not None}
        livro = service.editar_livro(id_livro, dados_filtrados)
        return _livro_to_dict(livro)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.get("/api/livros/isbn/{isbn}")
def detalhes_livro(isbn: str):
    """Visualiza detalhes de livros agrupados por ISBN."""
    service = LivroContainer.get_service()
    try:
        detalhes = service.visualizar_detalhes_livro(isbn)
        return {
            'isbn': detalhes['isbn'],
            'titulo': detalhes['titulo'],
            'autores': detalhes['autores'],
            'pais': detalhes['pais'],
            'editora': detalhes['editora'],
            'edicao': detalhes['edicao'],
            'total_exemplares': detalhes['total_exemplares'],
            'disponiveis': detalhes['disponiveis'],
            'emprestados': detalhes['emprestados'],
            'exemplares': [_livro_to_dict(e) for e in detalhes['exemplares']],
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.post("/api/livros/{id_livro}/estoque", response_model=LivroResponseSchema)
def atualizar_estoque(id_livro: int, isbn: str = Query(...)):
    """Atualiza status do livro: disponivel <-> emprestado."""
    service = LivroContainer.get_service()
    try:
        livro = service.atualizar_estoque(isbn, id_livro)
        return _livro_to_dict(livro)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@api.get("/api/livros/validar/{isbn}")
def validar_isbn(isbn: str):
    """Valida se o ISBN informado e valido."""
    service = LivroContainer.get_service()
    valido = service.validar_livro(isbn)
    return {'isbn': isbn, 'valido': valido}
