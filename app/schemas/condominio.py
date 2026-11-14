"""Schemas do condomínio: o formato dos dados que entram e saem da API.

Validam a entrada antes de chegar ao banco e definem o que a resposta mostra.
Não confundir com o modelo (app/models), que descreve a tabela.
"""
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class CondominioCriar(BaseModel):
    """Dados que o cliente informa ao cadastrar um condomínio.

    O id não entra aqui: quem o gera é o banco.
    """

    nome: str = Field(min_length=1, max_length=120)
    modo_aviso: Literal["todos", "destinatario_primeiro"] = "todos"


class CondominioLer(BaseModel):
    """Dados que a API devolve sobre um condomínio (inclui o id)."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    modo_aviso: str