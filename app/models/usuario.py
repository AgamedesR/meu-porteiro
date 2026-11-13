from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    condominio_id: Mapped[int] = mapped_column(ForeignKey("condominios.id"))
    nome: Mapped[str] = mapped_column(String(120))
    papel: Mapped[str] = mapped_column(String(20))
    ativo: Mapped[bool] = mapped_column(default=True)
