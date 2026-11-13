"""Morador: pessoa cadastrada em uma unidade, que recebe os avisos.

O campo ativo permite desativar quem se mudou sem apagar o histórico.
O telefone é texto para preservar zeros e símbolos.
"""

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base

if TYPE_CHECKING:
    from app.models.unidade import Unidade

class Morador(Base):
    __tablename__ = "moradores"

    id: Mapped[int] = mapped_column(primary_key=True)
    unidade_id: Mapped[int] = mapped_column(ForeignKey("unidades.id"))
    nome: Mapped[str] = mapped_column(String(120))
    telefone: Mapped[str] = mapped_column(String(20))
    ativo: Mapped[bool] = mapped_column(default=True)

    unidade: Mapped["Unidade"] = relationship(back_populates="moradores")