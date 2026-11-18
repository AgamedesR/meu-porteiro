"""Rotas HTTP dos usuários, aninhadas dentro do condomínio."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.usuario import UsuarioCriar, UsuarioLer
from app.services import usuario as service

router = APIRouter(
    prefix="/condominios/{condominio_id}/usuarios", tags=["usuarios"]
)


@router.post(
    "",
    response_model=UsuarioLer,
    status_code=status.HTTP_201_CREATED,
    responses={404: {"description": "Condomínio não encontrado"}},
)
def criar(condominio_id: int, dados: UsuarioCriar, db: Session = Depends(get_db)):
    """Cadastra um porteiro ou síndico no condomínio."""
    return service.criar_usuario(db, condominio_id, dados)


@router.get(
    "",
    response_model=list[UsuarioLer],
    responses={404: {"description": "Condomínio não encontrado"}},
)
def listar(
    condominio_id: int, apenas_ativos: bool = True, db: Session = Depends(get_db)
):
    """Lista os usuários do condomínio. Use ?apenas_ativos=false para todos."""
    return service.listar_usuarios(db, condominio_id, apenas_ativos)