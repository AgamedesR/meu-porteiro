"""Conexão com o banco: engine, sessões e a Base dos modelos.

A convenção de nomes dá nome previsível às constraints, o que o Alembic
precisa para alterá-las em migrações futuras.
"""

from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

convencao = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine, autoflush=False)


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=convencao)


def get_db():
    """Abre uma sessão por requisição e a fecha ao terminar, mesmo se der erro."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()