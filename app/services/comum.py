"""Verificações compartilhadas por vários services."""
from sqlalchemy.orm import Session

from app.exceptions import NaoEncontrado
from app.models.condominio import Condominio


def exigir_condominio(db: Session, condominio_id: int) -> None:
    """Levanta erro se o condomínio não existir."""
    if db.get(Condominio, condominio_id) is None:
        raise NaoEncontrado("Condomínio não encontrado")