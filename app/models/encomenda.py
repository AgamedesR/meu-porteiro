from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base

if TYPE_CHECKING:
    from app.models.condominio import Condominio
    from app.models.morador import Morador
    from app.models.unidade import Unidade

class Encomenda(Base):
    __tablename__ = "encomendas"

    id: Mapped[int] = mapped_column(primary_key=True)
    condominio_id: Mapped[int] = mapped_column(ForeignKey("condominios.id"))
    unidade_id: Mapped[int] = mapped_column(ForeignKey("unidades.id"))
    destinatario_id: Mapped[int | None] = mapped_column(ForeignKey("moradores.id"))
    destinatario_nome: Mapped[str | None] = mapped_column(String(120))
    transportadora: Mapped[str | None] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(20), default="recebida")
    codigo_retirada: Mapped[str] = mapped_column(String(4), index=True)
    recebida_em: Mapped[datetime] = mapped_column(default=datetime.now)
    avisada_em: Mapped[datetime | None]

    condominio: Mapped["Condominio"] = relationship()
    unidade: Mapped["Unidade"] = relationship(back_populates="encomendas")
    destinatario: Mapped["Morador"] = relationship()