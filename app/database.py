from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# URL do banco de dados (SQLite padrão, pode trocar depois)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./visto_americano.db")

# Criar engine (conexão com banco)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Criar SessionLocal (para usar em queries)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()

# Dependency para usar nas rotas (FastAPI)
def get_db():
    """Cria uma sessão do banco de dados que fecha automaticamente."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
