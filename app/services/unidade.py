"""Regras de negócio da unidade.

Toda operação recebe o condomínio e só enxerga as unidades dele, o que
mantém os dados de um prédio isolados dos de outro.
"""
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import Conflito
from app.models.unidade import Unidade
from app.schemas.unidade import UnidadeCriar
from app.services.comum import exigir_condominio


def criar_unidade(db: Session, condominio_id: int, dados: UnidadeCriar) -> Unidade:
    """Cadastra uma unidade no condomínio; o número não pode se repetir nele."""
    exigir_condominio(db, condominio_id)
    unidade = Unidade(
        condominio_id=condominio_id, andar=dados.andar, numero=dados.numero
    )
    db.add(unidade)
    try:
        db.commit()
    except IntegrityError:
        # A palavra final é do banco: o UniqueConstraint (condominio_id, numero)
        # recusa a duplicata, e o rollback deixa a sessão utilizável de novo
        db.rollback()
        raise Conflito(f"A unidade {dados.numero} já existe neste condomínio")
    db.refresh(unidade)
    return unidade


def listar_unidades(db: Session, condominio_id: int) -> list[Unidade]:
    """Lista as unidades do condomínio, por andar e número."""
    exigir_condominio(db, condominio_id)
    consulta = (
        select(Unidade)
        .where(Unidade.condominio_id == condominio_id)
        .order_by(Unidade.andar, Unidade.numero)
    )
    return list(db.scalars(consulta))