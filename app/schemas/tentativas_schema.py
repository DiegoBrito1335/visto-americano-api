from typing import List
from pydantic import BaseModel

class TentativaCriar(BaseModel):
    tipo: str          # "ds160" ou "entrevista"
    respostas: List[dict]

class TentativaResposta(BaseModel):
    id: int
    acertos: int
    total: int
    resultados: List[dict]

    class Config:
        from_attributes = True


class TentativaHistoricoItem(BaseModel):
    id: int
    tipo: str
    acertos: int
    total: int
    data: str

    class Config:
        from_attributes = True


class TentativaDetalhe(BaseModel):
    id: int
    tipo: str
    acertos: int
    total: int
    data: str

    class Config:
        from_attributes = True


class TentativaComparacao(BaseModel):
    total_tentativas: int
    media_acertos: float
    media_total_perguntas: float
    melhor_tentativa: dict
    pior_tentativa: dict

    class Config:
        from_attributes = True
