# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import auth, tentativas, usuarios, perguntas, pagamentos, pdf
from app.database import init_db


def build_cors_list():
    """
    Monta dinamicamente a lista de origens permitidas.
    Inclui automaticamente versões HTTP/HTTPS da FRONTEND_URL.
    """

    origins = set()

    # URL principal vinda do .env
    if settings.FRONTEND_URL:
        origins.add(settings.FRONTEND_URL)

        # Adicionar versões HTTP/HTTPS automaticamente
        if settings.FRONTEND_URL.startswith("http://"):
            https_version = settings.FRONTEND_URL.replace("http://", "https://")
            origins.add(https_version)

        if settings.FRONTEND_URL.startswith("https://"):
            http_version = settings.FRONTEND_URL.replace("https://", "http://")
            origins.add(http_version)

    # URLs para desenvolvimento
    origins.add("http://localhost:3000")
    origins.add("http://127.0.0.1:3000")

    # Railway/Render — opcional abrir tudo no desenvolvimento
    if settings.ENVIRONMENT == "development":
        origins.add("*")

    return list(origins)


def create_app():
    app = FastAPI(title=settings.APP_NAME)

    # ====================================================
    # DATABASE INIT (CORREÇÃO CRÍTICA)
    # ====================================================
    @app.on_event("startup")
    def startup_event():
        init_db()  # 🔥 GARANTE QUE AS TABELAS EXISTEM

    # ====================================================
    # CORS
    # ====================================================
    allowed_origins = build_cors_list()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ====================================================
    # Rotas
    # ====================================================
    app.include_router(auth.router)
    app.include_router(usuarios.router)
    app.include_router(perguntas.router)
    app.include_router(tentativas.router)
    app.include_router(pagamentos.router)
    app.include_router(pdf.router)

    @app.get("/")
    def root():
        return {
            "status": "online",
            "environment": settings.ENVIRONMENT,
            "allowed_origins": allowed_origins,
        }

    return app


app = create_app()
