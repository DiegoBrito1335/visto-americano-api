from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

import sentry_sdk
from prometheus_fastapi_instrumentator import Instrumentator

from app.core.config import settings
from app.database import Base, engine
from app.api.router import api_router


# ----------------------------------------
# SENTRY (MANTIDO)
# ----------------------------------------
sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0
)


# ----------------------------------------
# LIFESPAN
# ----------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    print("✅ Banco de dados inicializado e tabelas criadas.")
    yield
    print("👋 Encerrando aplicação...")


# ----------------------------------------
# APP
# ----------------------------------------
app = FastAPI(
    title="Visto Americano API",
    description="Backend oficial do sistema Visto Americano.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)


# ----------------------------------------
# CORS – APENAS PARA O PROJETO **VISTO AMERICANO**
# ----------------------------------------
allowed_origins = [
    "https://www.aprovistoamericano.com.br",
    "https://aprovistoamericano.com.br",
    "https://visto-americano.vercel.app",
    "http://localhost:3000",       # frontend local do Visto Americano
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------------------
# ROTAS
# ----------------------------------------
app.include_router(api_router, prefix="/api/v1")


@app.get("/", tags=["system"])
async def root():
    return {
        "message": "Visto Americano API Running",
        "version": "1.0.0",
        "docs": "/docs",
        "api_prefix": "/api/v1",
        "developer": "Diego Santos de Brito"
    }


@app.get("/health", tags=["system"])
async def health_check():
    return {
        "status": "healthy",
        "database": "connected"
    }
