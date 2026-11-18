"""Schemas do usuário."""
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class UsuarioCriar(BaseModel):
    """Dados informados ao cadastrar um usuário. O condomínio vem da URL."""

    nome: str = Field(min_length=1, max_length=120)
    papel: Literal["porteiro", "sindico"]


class UsuarioLer(BaseModel):
    """Dados devolvidos sobre um usuário."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    condominio_id: int
    nome: str
    papel: str
    ativo: bool