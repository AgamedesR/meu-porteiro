from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.condominio import Condominio
from app.schemas.condominio import CondominioCriar


def criar_condominio(db: Session, dados: CondominioCriar) -> Condominio:
    condominio = Condominio(nome=dados.nome, modo_aviso=dados.modo_aviso)
    db.add(condominio)
    db.commit()
    db.refresh(condominio)
    return condominio


def listar_condominios(db: Session) -> list[Condominio]:
    return list(db.scalars(select(Condominio).order_by(Condominio.nome)))