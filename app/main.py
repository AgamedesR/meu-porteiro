"""Ponto de entrada da API do Meu Porteiro.

Cria a aplicação FastAPI e registra os routers de cada recurso.
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions import Conflito, NaoEncontrado
from app.routers import condominio, unidade

app = FastAPI(title="Meu Porteiro")


@app.exception_handler(NaoEncontrado)
async def tratar_nao_encontrado(request: Request, exc: NaoEncontrado):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(Conflito)
async def tratar_conflito(request: Request, exc: Conflito):
    return JSONResponse(status_code=409, content={"detail": str(exc)})


app.include_router(condominio.router)
app.include_router(unidade.router)


@app.get("/saude")
def saude():
    """Verifica se a API está no ar."""
    return {"status": "ok"}