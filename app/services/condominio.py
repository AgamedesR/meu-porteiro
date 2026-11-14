"""Regras de negócio do condomínio.

Recebe schemas e uma sessão do banco e devolve modelos. Não conhece HTTP:
quem fala com o mundo externo é o router.
"""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.condominio import Condominio
from app.schemas.condominio import CondominioCriar


def criar_condominio(db: Session, dados: CondominioCriar) -> Condominio:
    """Grava um novo condomínio e o devolve já com o id gerado pelo banco."""
    condominio = Condominio(nome=dados.nome, modo_aviso=dados.modo_aviso)
    db.add(condominio)
    db.commit()
    db.refresh(condominio)
    return condominio


def listar_condominios(db: Session) -> list[Condominio]:
    """Devolve todos os condomínios, em ordem alfabética pelo nome."""
    return list(db.scalars(select(Condominio).order_by(Condominio.nome)))