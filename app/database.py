import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# ============================================================
# DEFINIR DATABASE_URL — PRIORIDADE:
# 1) PostgreSQL do Railway (.env)
# 2) SQLite local como fallback
# ============================================================

DATABASE_URL = settings.DATABASE_URL

if not DATABASE_URL or DATABASE_URL.strip() == "":
    # SQLite local como fallback seguro
    DATABASE_URL = "sqlite:///./local.db"

# ============================================================
# ENGINE
# Configuração automática dependendo do tipo de banco
# ============================================================

# Caso seja SQLite ------------------------------
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},  # obrigatório no SQLite
        pool_pre_ping=True
    )

# Caso seja PostgreSQL --------------------------
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
# BASE
# ============================================================

Base = declarative_base()

# ============================================================
# INIT DB — usado pelo create_app()
# ============================================================

def init_db():
    """
    Cria as tabelas automaticamente no banco.
    - Em produção: PostgreSQL (Railway)
    - Em desenvolvimento: SQLite local
    """
    import app.models  # garante que os models sejam carregados
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
