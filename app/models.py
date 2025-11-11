from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Usuario(Base):
    """Tabela de usuários do sistema"""
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    senha_hash = Column(String, nullable=False)
    nome_completo = Column(String)
    tipo_plano = Column(String, default="gratuito")  # gratuito ou premium
    data_cadastro = Column(DateTime, default=datetime.utcnow)
    data_expiracao_premium = Column(DateTime, nullable=True)
    ativo = Column(Boolean, default=True)
    
    # Relacionamento
    tentativas = relationship("Tentativa", back_populates="usuario")


class PerguntaDS160(Base):
    """Perguntas do formulário DS-160"""
    __tablename__ = "perguntas_ds160"
    
    id = Column(Integer, primary_key=True, index=True)
    categoria = Column(String, index=True)  # pessoal, viagem, trabalho, familia, seguranca
    pergunta_texto = Column(String, nullable=False)
    tipo_resposta = Column(String, default="texto")  # texto, multipla_escolha, sim_nao
    opcoes = Column(JSON, nullable=True)  # ["Opção 1", "Opção 2"] para múltipla escolha
    resposta_ideal = Column(String, nullable=True)  # Orientação de resposta
    peso_avaliacao = Column(Integer, default=5)  # 1-10: importância para aprovação
    dica = Column(String, nullable=True)
    gratuita = Column(Boolean, default=False)  # ✅ CORRIGIDO: gratuita (com 'a')
    ordem = Column(Integer, default=0)


class PerguntaEntrevista(Base):
    """Perguntas comuns em entrevistas na embaixada"""
    __tablename__ = "perguntas_entrevista"
    
    id = Column(Integer, primary_key=True, index=True)
    categoria = Column(String, index=True)  # vinculos, financeiro, viagem, pessoal
    pergunta_texto = Column(String, nullable=False)
    resposta_ideal = Column(String, nullable=True)
    palavras_positivas = Column(JSON, nullable=True)  # ["trabalho", "família", "propriedade"]
    palavras_negativas = Column(JSON, nullable=True)  # ["talvez", "não sei"]
    peso_avaliacao = Column(Integer, default=5)
    dica = Column(String, nullable=True)
    gratuita = Column(Boolean, default=False)  # ✅ CORRIGIDO: gratuita (com 'a')
    ordem = Column(Integer, default=0)


class Tentativa(Base):
    """Registro de cada simulação feita pelo usuário"""
    __tablename__ = "tentativas"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    tipo = Column(String)  # "ds160", "entrevista", "completo"
    data_tentativa = Column(DateTime, default=datetime.utcnow)
    pontuacao_final = Column(Float)
    pontuacao_categorias = Column(JSON)  # {"vinculos": 80, "financeiro": 60, ...}
    probabilidade = Column(String)  # "Baixa", "Média", "Alta"
    tempo_gasto = Column(Integer, default=0)  # segundos
    completo = Column(Boolean, default=False)
    
    # Relacionamento
    usuario = relationship("Usuario", back_populates="tentativas")
    respostas = relationship("Resposta", back_populates="tentativa")


class Resposta(Base):
    """Respostas individuais de cada pergunta"""
    __tablename__ = "respostas"
    
    id = Column(Integer, primary_key=True, index=True)
    tentativa_id = Column(Integer, ForeignKey("tentativas.id"))
    pergunta_id = Column(Integer)  # ID da pergunta (DS160 ou Entrevista)
    tipo_pergunta = Column(String)  # "ds160" ou "entrevista"
    resposta_usuario = Column(String)
    pontos_obtidos = Column(Float)
    feedback = Column(String, nullable=True)
    
    # Relacionamento
    tentativa = relationship("Tentativa", back_populates="respostas")