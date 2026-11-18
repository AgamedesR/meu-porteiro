"""Preparações compartilhadas pelos testes.

Cada teste recebe uma API ligada a um banco SQLite em memória, criado do
zero e descartado no fim, o que isola os testes uns dos outros.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.models  # noqa: F401  (registra os modelos no Base)
from app.db import Base, get_db
from app.main import app


@pytest.fixture()
def client():
    """Cliente HTTP de teste, ligado a um banco novo em memória."""
    # StaticPool mantém uma única conexão, senão cada thread veria um
    # banco em memória diferente (e vazio)
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    sessao_de_teste = sessionmaker(bind=engine, autoflush=False)

    def get_db_de_teste():
        db = sessao_de_teste()
        try:
            yield db
        finally:
            db.close()

    # Troca o get_db real pelo de teste, só enquanto o teste roda
    app.dependency_overrides[get_db] = get_db_de_teste
    with TestClient(app) as cliente:
        yield cliente
    app.dependency_overrides.clear()
    engine.dispose()


@pytest.fixture()
def condominio(client):
    """Um condomínio já cadastrado."""
    return client.post("/condominios", json={"nome": "Edifício Aurora"}).json()


@pytest.fixture()
def outro_condominio(client):
    """Um segundo condomínio, para testar o isolamento entre prédios."""
    return client.post("/condominios", json={"nome": "Residencial Sol"}).json()


@pytest.fixture()
def unidade(client, condominio):
    """A unidade 901, cadastrada no primeiro condomínio."""
    resposta = client.post(
        f"/condominios/{condominio['id']}/unidades",
        json={"andar": 9, "numero": "901"},
    )
    return resposta.json()


@pytest.fixture()
def unidade_do_outro(client, outro_condominio):
    """A unidade 901, cadastrada no segundo condomínio."""
    resposta = client.post(
        f"/condominios/{outro_condominio['id']}/unidades",
        json={"andar": 9, "numero": "901"},
    )
    return resposta.json()
