"""Rotas HTTP do condomínio.

Só recebe a requisição, chama o service e devolve a resposta.
Não contém regra de negócio.
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.condominio import CondominioCriar, CondominioLer
from app.services import condominio as service

router = APIRouter(prefix="/condominios", tags=["condominios"])


@router.post("", response_model=CondominioLer, status_code=status.HTTP_201_CREATED)
def criar(dados: CondominioCriar, db: Session = Depends(get_db)):
    """Cadastra um condomínio. O modo de aviso é opcional (padrão: todos)."""
    return service.criar_condominio(db, dados)


@router.get("", response_model=list[CondominioLer])
def listar(db: Session = Depends(get_db)):
    """Lista os condomínios cadastrados, em ordem alfabética."""
    return service.listar_condominios(db)