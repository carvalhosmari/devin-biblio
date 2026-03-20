import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bibliomania.settings')
django.setup()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from emprestimo.container import EmprestimoContainer

api = FastAPI(title="Bibliomania Emprestimo API", version="1.0.0")


class EmprestimoCreateSchema(BaseModel):
    id_leitor: int
    id_livro: int


class EmprestimoResponseSchema(BaseModel):
    id: int
    id_leitor: int
    id_livro: int
    data_emprestimo: str
    data_devolucao: str | None = None
    data_limite: str
    status: str
    renovacoes: int

    class Config:
        from_attributes = True


def _emprestimo_to_dict(emp) -> dict:
    return {
        'id': emp.id,
        'id_leitor': emp.id_leitor_id,
        'id_livro': emp.id_livro_id,
        'data_emprestimo': emp.data_emprestimo.isoformat(),
        'data_devolucao': emp.data_devolucao.isoformat() if emp.data_devolucao else None,
        'data_limite': emp.data_limite.isoformat(),
        'status': emp.status,
        'renovacoes': emp.renovacoes,
    }


@api.get("/api/emprestimos", response_model=list[EmprestimoResponseSchema])
def listar_emprestimos(id_leitor: int | None = None):
    """Lista emprestimos ativos, opcionalmente filtrados por leitor."""
    service = EmprestimoContainer.get_service()
    emprestimos = service.visualizar_emprestimos_ativos(id_leitor)
    return [_emprestimo_to_dict(e) for e in emprestimos]


@api.post("/api/emprestimos", response_model=EmprestimoResponseSchema, status_code=201)
def registrar_emprestimo(dados: EmprestimoCreateSchema):
    """Registra um novo emprestimo."""
    service = EmprestimoContainer.get_service()
    try:
        emprestimo = service.registrar_emprestimo(dados.id_leitor, dados.id_livro)
        return _emprestimo_to_dict(emprestimo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@api.post("/api/emprestimos/{id_emprestimo}/devolver")
def registrar_devolucao(id_emprestimo: int):
    """Registra a devolucao de um livro."""
    service = EmprestimoContainer.get_service()
    try:
        resultado = service.registrar_devolucao(id_emprestimo)
        emp = resultado['emprestimo']
        return {
            'emprestimo': _emprestimo_to_dict(emp),
            'multa': float(resultado['multa']),
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@api.post("/api/emprestimos/{id_emprestimo}/renovar", response_model=EmprestimoResponseSchema)
def renovar_emprestimo(id_emprestimo: int):
    """Renova o emprestimo por mais 14 dias."""
    service = EmprestimoContainer.get_service()
    try:
        novo = service.renovar_emprestimo(id_emprestimo)
        return _emprestimo_to_dict(novo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@api.get("/api/emprestimos/{id_emprestimo}/prazo")
def validar_prazo(id_emprestimo: int):
    """Verifica o status do prazo do emprestimo."""
    service = EmprestimoContainer.get_service()
    try:
        info = service.validar_prazo(id_emprestimo)
        return {
            'emprestimo': _emprestimo_to_dict(info['emprestimo']),
            'atrasado': info['atrasado'],
            'dias_restantes': info['dias_restantes'],
            'dias_atraso': info['dias_atraso'],
            'multa': float(info['multa']),
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
