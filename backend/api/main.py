"""
FastAPI - Ponto de entrada da API REST do Bibliomania.
Integra com Django ORM para acesso ao banco de dados.
"""

import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bibliomania.settings")
django.setup()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import emprestimo, leitor, livro

app = FastAPI(
    title="Bibliomania API",
    description="API REST para o sistema de gestao de biblioteca Bibliomania",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:5173").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(leitor.router, prefix="/api/leitor", tags=["Leitor"])
app.include_router(livro.router, prefix="/api/livro", tags=["Livro"])
app.include_router(emprestimo.router, prefix="/api/emprestimo", tags=["Emprestimo"])


@app.get("/")
def root():
    """Endpoint raiz da API."""
    return {"message": "Bibliomania API v0.1.0"}
