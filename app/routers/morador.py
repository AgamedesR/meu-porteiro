"""Rotas HTTP dos moradores, aninhadas dentro do condomínio.

Só recebe a requisição, chama o service e devolve a resposta.
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.morador import MoradorCriar, MoradorLer
from app.services import morador as service

router = APIRouter(
    prefix="/condominios/{condominio_id}/moradores", tags=["moradores"]
)


@router.post(
    "",
    response_model=MoradorLer,
    status_code=status.HTTP_201_CREATED,
    responses={404: {"description": "Condomínio ou unidade não encontrados"}},
)
def criar(condominio_id: int, dados: MoradorCriar, db: Session = Depends(get_db)):
    """Cadastra um morador em uma unidade do condomínio."""
    return service.criar_morador(db, condominio_id, dados)


@router.get(
    "",
    response_model=list[MoradorLer],
    responses={404: {"description": "Condomínio não encontrado"}},
)
def listar(
    condominio_id: int,
    unidade_id: int | None = None,
    apenas_ativos: bool = True,
    db: Session = Depends(get_db),
):
    """Lista os moradores do condomínio.

    Filtros opcionais na URL: ?unidade_id=1 e ?apenas_ativos=false.
    """
    return service.listar_moradores(db, condominio_id, unidade_id, apenas_ativos)