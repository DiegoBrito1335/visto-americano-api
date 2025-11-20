from pydantic import BaseModel

class PerguntaEntrevistaResposta(BaseModel):
    id: int
    pergunta: str
    categoria: str
    gratuito: bool

    class Config:
        from_attributes = True

class PerguntaDS160Resposta(BaseModel):
    id: int
    secao: str
    pergunta: str

    class Config:
        from_attributes = True
