from pydantic import BaseModel
from typing import List, Optional


# =======================
#   DS-160
# =======================
class PerguntaDS160Resposta(BaseModel):
    id: int
    categoria: str
    pergunta_texto: str
    tipo_resposta: Optional[str] = None
    opcoes: Optional[List[str]] = None
    resposta_ideal: Optional[str] = None
    peso_avaliacao: int
    dica: Optional[str] = None
    gratuita: bool
    ordem: int

    class Config:
        orm_mode = True


# =======================
#   ENTREVISTA
# =======================
class PerguntaEntrevistaResposta(BaseModel):
    id: int
    categoria: str
    pergunta_texto: str
    resposta_ideal: Optional[str] = None
    palavras_positivas: Optional[List[str]] = None
    palavras_negativas: Optional[List[str]] = None
    peso_avaliacao: int
    dica: Optional[str] = None
    gratuita: bool
    ordem: int

    class Config:
        orm_mode = True
