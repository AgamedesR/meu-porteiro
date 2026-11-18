"""Regras de negócio do usuário (porteiro e síndico)."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCriar
from app.services.comum import exigir_condominio


def criar_usuario(db: Session, condominio_id: int, dados: UsuarioCriar) -> Usuario:
    """Cadastra um usuário no condomínio."""
    exigir_condominio(db, condominio_id)
    usuario = Usuario(
        condominio_id=condominio_id, nome=dados.nome, papel=dados.papel
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


def listar_usuarios(
    db: Session, condominio_id: int, apenas_ativos: bool = True
) -> list[Usuario]:
    """Lista os usuários do condomínio, em ordem alfabética."""
    exigir_condominio(db, condominio_id)
    consulta = (
        select(Usuario)
        .where(Usuario.condominio_id == condominio_id)
        .order_by(Usuario.nome)
    )
    if apenas_ativos:
        consulta = consulta.where(Usuario.ativo.is_(True))
    return list(db.scalars(consulta))