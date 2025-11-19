from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict
from datetime import datetime

# ============================================================
#                       USUÁRIOS
# ============================================================

class UsuarioBase(BaseModel):
    email: EmailStr
    nome_completo: str


class UsuarioCriar(UsuarioBase):
    senha: str = Field(..., min_length=6, max_length=72)

class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str    


class UsuarioResposta(UsuarioBase):
    id: int
    tipo_plano: str
    data_cadastro: datetime
    data_expiracao_premium: Optional[datetime] = None
    ativo: bool

    class Config:
        from_attributes = True


# ============================================================
#                       AUTENTICAÇÃO
# ============================================================

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


# ============================================================
#                       PERGUNTAS DS-160
# ============================================================

class PerguntaDS160Base(BaseModel):
    categoria: str
    pergunta_texto: str
    tipo_resposta: str = "texto"
    opcoes: Optional[List[str]] = None
    resposta_ideal: Optional[str] = None
    peso_avaliacao: int = 5
    dica: Optional[str] = None
    gratuita: bool = False
    ordem: int = 0


class PerguntaDS160Resposta(PerguntaDS160Base):
    id: int

    class Config:
        from_attributes = True


# ============================================================
#                   PERGUNTAS ENTREVISTA
# ============================================================

class PerguntaEntrevistaBase(BaseModel):
    categoria: str
    pergunta_texto: str
    resposta_ideal: Optional[str] = None
    palavras_positivas: Optional[List[str]] = None
    palavras_negativas: Optional[List[str]] = None
    peso_avaliacao: int = 5
    dica: Optional[str] = None
    gratuita: bool = False
    ordem: int = 0


class PerguntaEntrevistaResposta(PerguntaEntrevistaBase):
    id: int

    class Config:
        from_attributes = True


# ============================================================
#                           TENTATIVAS
# ============================================================

class RespostaUsuario(BaseModel):
    pergunta_id: int
    tipo_pergunta: str      # "ds160" | "entrevista"
    resposta_usuario: str


class TentativaCriar(BaseModel):
    tipo: str               # "ds160" | "entrevista" | "completo"
    respostas: List[RespostaUsuario]
    tempo_gasto: Optional[int] = 0


class TentativaResposta(BaseModel):
    id: int
    tipo: str
    data_tentativa: datetime
    pontuacao_final: float
    pontuacao_categorias: Optional[Dict[str, float]] = None
    probabilidade: str
    tempo_gasto: int
    completo: bool

    class Config:
        from_attributes = True


# ============================================================
#                      RESULTADO DA AVALIAÇÃO
# ============================================================

class ResultadoAvaliacao(BaseModel):
    tentativa_id: int
    pontuacao_geral: float
    probabilidade: str
    pontuacao_categorias: Dict[str, float]
    pontos_fortes: List[str]
    pontos_fracos: List[str]
    recomendacoes: List[str]
    total_perguntas: int
    perguntas_respondidas: int


# ============================================================
#                HISTÓRICO / DETALHE / EVOLUÇÃO
# ============================================================

class TentativaHistoricoItem(BaseModel):
    id: int
    data: str
    hora: str
    tipo: str
    pontuacao: float
    probabilidade: str
    completo: bool


class TentativaDetalheResposta(BaseModel):
    id: int
    pergunta: str
    resposta: str
    tipo_pergunta: str


class TentativaDetalhe(BaseModel):
    id: int
    data: str
    tipo: str
    pontuacao_final: float
    probabilidade: str
    pontuacao_categorias: Dict[str, float]
    respostas: List[TentativaDetalheResposta]


class TentativaComparacaoItem(BaseModel):
    data: str
    pontuacao: float
    probabilidade: str
    tipo: str


class TentativaComparacao(BaseModel):
    total: int
    evolucao: List[TentativaComparacaoItem]
    estatisticas: Dict[str, float]

