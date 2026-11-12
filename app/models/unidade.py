from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.condominio import Condominio

class Unidade(Base):
    __tablename__ = "unidades"
    __table_args__ = (UniqueConstraint("condominio_id", "numero"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    condominio_id: Mapped[int] = mapped_column(ForeignKey("condominios.id"))
    andar: Mapped[int]
    numero: Mapped[str] = mapped_column(String(10))

    condominio: Mapped["Condominio"] = relationship(back_populates="unidades")