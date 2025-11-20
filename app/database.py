import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# ============================================================
# DEFINIR DATABASE_URL — PRIORIDADE:
# 1) Railway (PostgreSQL)
# 2) SQLite local como fallback
# ============================================================

DATABASE_URL = settings.DATABASE_URL

if not DATABASE_URL or DATABASE_URL.strip() == "":
    DATABASE_URL = "sqlite:///./local.db"

# ============================================================
# ENGINE (configuração automática)
# ============================================================

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        pool_pre_ping=True
    )
else:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
        pool_recycle=1800,
    )

# ============================================================
# SESSION
# ============================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ============================================================
# BASE ORM
# ============================================================

Base = declarative_base()

# ============================================================
# INIT DB — CRIA AS TABELAS AUTOMATICAMENTE
# ============================================================

def init_db():
    """
    Garante que todos os models são importados e criados no banco.
    """
    import app.models  # NECESSÁRIO: força carregamento dos models
    Base.metadata.create_all(bind=engine)

# ============================================================
# DEPENDÊNCIA DO FASTAPI
# ============================================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
