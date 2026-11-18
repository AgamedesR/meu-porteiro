"""Regras de negócio da unidade.

Toda operação recebe o condomínio e só enxerga as unidades dele, o que
mantém os dados de um prédio isolados dos de outro.
"""
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import Conflito, NaoEncontrado
from app.models.condominio import Condominio
from app.models.unidade import Unidade
from app.schemas.unidade import UnidadeCriar

def _exigir_condominio(db: Session, condominio_id: int) -> None:
    """Levanta erro se o condomínio não existir."""
    # db.get busca pela chave primária e devolve None se não achar
    if db.get(Condominio, condominio_id) is None:
        raise NaoEncontrado("Condomínio não encontrado")


def criar_unidade(db: Session, condominio_id: int, dados: UnidadeCriar) -> Unidade:
    """Cadastra uma unidade no condomínio; o número não pode se repetir nele."""
    _exigir_condominio(db, condominio_id)
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
    _exigir_condominio(db, condominio_id)
    consulta = (
        select(Unidade)
        .where(Unidade.condominio_id == condominio_id)
        .order_by(Unidade.andar, Unidade.numero)
    )
    return list(db.scalars(consulta))