"""Schemas do morador."""
import re

from pydantic import BaseModel, ConfigDict, Field, field_validator


class MoradorCriar(BaseModel):
    """Dados informados ao cadastrar um morador.

    O condomínio vem da URL; a unidade vem aqui e será conferida no service.
    """

    unidade_id: int
    nome: str = Field(min_length=1, max_length=120)
    telefone: str

    @field_validator("telefone")
    @classmethod
    def normalizar_telefone(cls, valor: str) -> str:
        """Guarda só os dígitos, aceitando entradas como (83) 99999-0000."""
        digitos = re.sub(r"\D", "", valor)
        if not 10 <= len(digitos) <= 13:
            raise ValueError("O telefone deve ter de 10 a 13 dígitos, com DDD")
        return digitos


class MoradorLer(BaseModel):
    """Dados devolvidos sobre um morador."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    unidade_id: int
    nome: str
    telefone: str
    ativo: bool