from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# ==============================================================
# ENGINE — usa a URL do config.py (que já lê .env automaticamente)
# ==============================================================

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,        # Evita desconexões do Railway
    pool_size=10,              # Tamanho inicial do pool
    max_overflow=20,           # Número máximo extra de conexões
    pool_recycle=1800,         # Renova conexões antigas
)

# ==============================================================
# SESSION
# ==============================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ==============================================================
# BASE
# ==============================================================

Base = declarative_base()

# ==============================================================
# DEPENDÊNCIA DO FASTAPI
# ==============================================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
