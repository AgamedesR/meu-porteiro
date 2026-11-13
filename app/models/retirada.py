"""Retirada: registro de que uma encomenda foi entregue.

Cada encomenda tem no máximo uma retirada (encomenda_id é único). Guarda o
porteiro que entregou, o horário e quem levou: um morador ou um terceiro
identificado pelo nome.
"""

from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base

if TYPE_CHECKING:
    from app.models.encomenda import Encomenda
    from app.models.usuario import Usuario
    from app.models.morador import Morador

class Retirada(Base):
    __tablename__ = "retiradas"

    id: Mapped[int] = mapped_column(primary_key=True)
    encomenda_id: Mapped[int] = mapped_column(ForeignKey("encomendas.id"), unique=True)
    porteiro_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    retirada_em: Mapped[datetime] = mapped_column(default=datetime.now)
    retirado_por_morador_id: Mapped[int | None] = mapped_column(ForeignKey("moradores.id"))
    retirado_por_nome: Mapped[str | None] = mapped_column(String(120))

    encomenda: Mapped["Encomenda"] = relationship(back_populates="retirada")
    porteiro: Mapped["Usuario"] = relationship()
    retirado_por: Mapped["Morador | None"] = relationship()
    