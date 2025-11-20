from pydantic import BaseModel

class PagamentoCreate(BaseModel):
    usuario_id: int
    status: str
    valor: float
