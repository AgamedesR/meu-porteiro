"""Condomínio: cada prédio cliente do sistema.

É a raiz da hierarquia: unidades, usuários e encomendas pertencem a um
condomínio, o que isola os dados de um prédio dos de outro.
modo_aviso define como os moradores são avisados (padrão: todos).
"""

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base

if TYPE_CHECKING:
    from app.models.unidade import Unidade

class Condominio(Base):
    __tablename__ = "condominios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(120))
    modo_aviso: Mapped[str] = mapped_column(String(30), default="todos")

    unidades: Mapped[list["Unidade"]] = relationship(back_populates="condominio")
