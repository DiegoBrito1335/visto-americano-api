# app/__init__.py
import os
from fastapi import FastAPI
from .database import init_db

# Routers
from .routers import auth as auth_router
from .routers import usuarios as usuarios_router
from .routers import perguntas as perguntas_router
from .routers import pagamentos as pagamentos_router
from .routers import pdf as pdf_router
from .routers import tentativas as tentativas_router

def create_app() -> FastAPI:
    app = FastAPI(title="Visto Americano API")

    # Iniciar DB (criar tabelas etc)
    try:
        init_db()
    except Exception:
        pass

    # Registrar rotas
    app.include_router(auth_router.router, prefix="/auth")
    app.include_router(usuarios_router.router, prefix="/usuarios")
    app.include_router(perguntas_router.router, prefix="/perguntas")
    app.include_router(pagamentos_router.router, prefix="/pagamentos")
    app.include_router(pdf_router.router, prefix="/pdf")
    app.include_router(tentativas_router.router, prefix="/tentativas")

    @app.get("/ping")
    def ping():
        return {"status": "ok"}

    return app
