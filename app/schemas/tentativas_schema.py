from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator
from datetime import datetime

# ============================================================
#                    RESPOSTAS (ENTRADA)
# ============================================================

class RespostaCreate(BaseModel):
    pergunta_id: int
    tipo_pergunta: str  # "ds160" ou "entrevista"
    resposta_usuario: str


# ============================================================
#                    TENTATIVA (ENTRADA)
# ============================================================

class TentativaCreate(BaseModel):
    tipo: str = Field(..., description="ds160 | entrevista | completo")
    respostas: List[RespostaCreate]
    tempo_gasto: int = 0


# ============================================================
#                    RESPOSTA (SAÍDA)
# ============================================================

class RespostaResposta(BaseModel):
    id: int
    pergunta_id: int
    tipo_pergunta: str
    resposta_usuario: str
    pontos_obtidos: float
    feedback: Optional[str]

    model_config = {"from_attributes": True}


# ============================================================
#                    TENTATIVA (SAÍDA)
# ============================================================

class TentativaResposta(BaseModel):
    id: int
    tipo: str
    data_tentativa: str
    pontuacao_final: float
    probabilidade: str
    pontuacao_categorias: Dict[str, Any]
    tempo_gasto: int
    completo: bool
    respostas: List[RespostaResposta]

    model_config = {"from_attributes": True}

    @field_validator("data_tentativa", mode="before")
    def convert_datetime(cls, value):
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        return str(value)


# ============================================================
#                    ESTATÍSTICAS
# ============================================================

class TentativaComparacao(BaseModel):
    total_tentativas: int
    media_nota: float
    nota_maxima: float
    nota_minima: float
    distribucao_probabilidade: Dict[str, int]

    model_config = {"from_attributes": True}


# ============================================================
#                HISTÓRICO DE TENTATIVAS
# ============================================================

class TentativaHistoricoItem(BaseModel):
    id: int
    tipo: str
    data_tentativa: str
    pontuacao_final: float
    probabilidade: str

    model_config = {"from_attributes": True}

    @field_validator("data_tentativa", mode="before")
    def convert_datetime(cls, value):
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        return str(value)


# ============================================================
#                DETALHE COMPLETO DA TENTATIVA
# ============================================================

class TentativaDetalhe(BaseModel):
    id: int
    tipo: str
    data_tentativa: str
    pontuacao_final: float
    probabilidade: str
    pontuacao_categorias: Dict[str, Any]
    tempo_gasto: int
    completo: bool
    respostas: List[RespostaResposta]

    model_config = {"from_attributes": True}

    @field_validator("data_tentativa", mode="before")
    def convert_datetime(cls, value):
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        return str(value)
