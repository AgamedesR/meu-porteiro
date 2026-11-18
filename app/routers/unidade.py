"""Rotas HTTP das unidades, aninhadas dentro do condomínio.

Só recebe a requisição, chama o service e devolve a resposta.
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.unidade import UnidadeCriar, UnidadeLer
from app.services import unidade as service

router = APIRouter(
    prefix="/condominios/{condominio_id}/unidades", tags=["unidades"]
)


@router.post(
    "",
    response_model=UnidadeLer,
    status_code=status.HTTP_201_CREATED,
    responses={
        404: {"description": "Condomínio não encontrado"},
        409: {"description": "Número já usado neste condomínio"},
    },
)
def criar(condominio_id: int, dados: UnidadeCriar, db: Session = Depends(get_db)):
    """Cadastra uma unidade no condomínio indicado na URL."""
    return service.criar_unidade(db, condominio_id, dados)


@router.get(
    "",
    response_model=list[UnidadeLer],
    responses={404: {"description": "Condomínio não encontrado"}},
)
def listar(condominio_id: int, db: Session = Depends(get_db)):
    """Lista as unidades do condomínio indicado na URL."""
    return service.listar_unidades(db, condominio_id)