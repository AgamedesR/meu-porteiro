from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class CondominioCriar(BaseModel):
    nome: str = Field(min_length=1, max_length=120)
    modo_aviso: Literal["todos", "destinatario_primeiro"] = "todos"


class CondominioLer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    modo_aviso: str