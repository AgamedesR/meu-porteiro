"""Regras de negócio do morador.

Garante que o morador só seja cadastrado em uma unidade do próprio
condomínio informado.
"""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.exceptions import NaoEncontrado
from app.models.morador import Morador
from app.models.unidade import Unidade
from app.schemas.morador import MoradorCriar
from app.services.comum import exigir_condominio


def criar_morador(db: Session, condominio_id: int, dados: MoradorCriar) -> Morador:
    """Cadastra um morador em uma unidade que pertença ao condomínio."""
    exigir_condominio(db, condominio_id)
    unidade = db.get(Unidade, dados.unidade_id)
    # A mesma mensagem vale para "não existe" e "é de outro condomínio",
    # para não revelar a existência de unidades de outros prédios
    if unidade is None or unidade.condominio_id != condominio_id:
        raise NaoEncontrado("Unidade não encontrada neste condomínio")

    morador = Morador(
        unidade_id=dados.unidade_id, nome=dados.nome, telefone=dados.telefone
    )
    db.add(morador)
    db.commit()
    db.refresh(morador)
    return morador


def listar_moradores(
    db: Session,
    condominio_id: int,
    unidade_id: int | None = None,
    apenas_ativos: bool = True,
) -> list[Morador]:
    """Lista os moradores do condomínio, com filtros opcionais."""
    exigir_condominio(db, condominio_id)
    # O join com Unidade permite filtrar pelo condomínio, já que o morador
    # só guarda a unidade
    consulta = (
        select(Morador)
        .join(Unidade, Morador.unidade_id == Unidade.id)
        .where(Unidade.condominio_id == condominio_id)
        .order_by(Morador.nome)
    )
    if unidade_id is not None:
        consulta = consulta.where(Morador.unidade_id == unidade_id)
    if apenas_ativos:
        consulta = consulta.where(Morador.ativo.is_(True))
    return list(db.scalars(consulta))