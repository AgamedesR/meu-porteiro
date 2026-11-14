"""Ponto de entrada da API do Meu Porteiro.

Cria a aplicação FastAPI e registra os routers de cada recurso.
"""
from fastapi import FastAPI

from app.routers import condominio

app = FastAPI(title="Meu Porteiro")

app.include_router(condominio.router)


@app.get("/saude")
def saude():
    """Verifica se a API está no ar."""
    return {"status": "ok"}