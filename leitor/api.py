import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bibliomania.settings')
django.setup()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from leitor.container import LeitorContainer

api = FastAPI(title="Bibliomania API", version="1.0.0")


class LeitorCreateSchema(BaseModel):
    nome: str
    cpf: str
    email: str
    telefone: str | None = None
    endereco: str | None = None
    ativo: bool = True


class LeitorUpdateSchema(BaseModel):
    nome: str | None = None
    cpf: str | None = None
    email: str | None = None
    telefone: str | None = None
    endereco: str | None = None
    ativo: bool | None = None


class LeitorResponseSchema(BaseModel):
    id: int
    nome: str
    cpf: str
    email: str
    telefone: str | None = None
    endereco: str | None = None
    data_cadastro: str
    ativo: bool

    class Config:
        from_attributes = True


def _leitor_to_dict(leitor) -> dict:
    return {
        'id': leitor.id,
        'nome': leitor.nome,
        'cpf': leitor.cpf,
        'email': leitor.email,
        'telefone': leitor.telefone,
        'endereco': leitor.endereco,
        'data_cadastro': leitor.data_cadastro.isoformat(),
        'ativo': leitor.ativo,
    }


@api.get("/api/leitores", response_model=list[LeitorResponseSchema])
def listar_leitores():
    """Lista todos os leitores cadastrados."""
    service = LeitorContainer.get_service()
    leitores = service.listar_leitores()
    return [_leitor_to_dict(l) for l in leitores]


@api.post("/api/leitores", response_model=LeitorResponseSchema, status_code=201)
def cadastrar_leitor(dados: LeitorCreateSchema):
    """Cadastra um novo leitor."""
    service = LeitorContainer.get_service()
    try:
        leitor = service.cadastrar_leitor(dados.model_dump(exclude_none=True))
        return _leitor_to_dict(leitor)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@api.put("/api/leitores/{id_leitor}", response_model=LeitorResponseSchema)
def atualizar_leitor(id_leitor: int, dados: LeitorUpdateSchema):
    """Atualiza os dados de um leitor existente."""
    service = LeitorContainer.get_service()
    try:
        dados_filtrados = {k: v for k, v in dados.model_dump().items() if v is not None}
        leitor = service.atualizar_leitor(id_leitor, dados_filtrados)
        return _leitor_to_dict(leitor)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.get("/api/leitores/{id_leitor}", response_model=LeitorResponseSchema)
def buscar_leitor(id_leitor: int):
    """Busca um leitor pelo ID."""
    service = LeitorContainer.get_service()
    try:
        perfil = service.acessar_historico_leitor(id_leitor)
        return _leitor_to_dict(perfil['leitor'])
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.get("/api/leitores/{id_leitor}/historico")
def historico_leitor(id_leitor: int):
    """Exibe o perfil do leitor e seu historico de emprestimos."""
    service = LeitorContainer.get_service()
    try:
        perfil = service.acessar_historico_leitor(id_leitor)
        return {
            'leitor': _leitor_to_dict(perfil['leitor']),
            'emprestimos': perfil['emprestimos'],
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
