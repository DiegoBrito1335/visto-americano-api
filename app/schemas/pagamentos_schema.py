from pydantic import BaseModel


class PagamentoCreate(BaseModel):
    valor: float
    metodo: str  # exemplo: "pix", "cartao", "stripe"
    plano: str   # "premium_mensal", "premium_anual"


class PagamentoResponse(BaseModel):
    id: int
    usuario_id: int
    valor: float
    status: str
    metodo: str
    plano: str

    class Config:
        from_attributes = True
