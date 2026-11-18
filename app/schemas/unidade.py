"""Schema da unidade."""
from pydantic import BaseModel, ConfigDict, Field


class UnidadeCriar(BaseModel):
    """Dados informados ao cadastrar uma unidade.

    O condomínio não entra aqui: vem da URL.
    """

    andar: int = Field(ge=0)
    numero: str = Field(min_length=1, max_length=10)

class UnidadeLer(BaseModel):
    """Dados devolvidos sobre uma unidade"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    condominio_id: int
    andar: int
    numero: str
