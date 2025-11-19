from fastapi import FastAPI

# IMPORTANDO OS ROUTERS
from app.routers.auth import router as auth_router
from app.routers.usuarios import router as usuarios_router
from app.routers.perguntas import router as perguntas_router
from app.routers.tentativas import router as tentativas_router
from app.routers.pagamentos import router as pagamentos_router
from app.routers.pdf import router as pdf_router


def create_app():
    app = FastAPI(title="Visto Americano API")

    # Registrando os routers (prefixos já estão definidos dentro de cada router)
    app.include_router(auth_router)
    app.include_router(usuarios_router)
    app.include_router(perguntas_router)
    app.include_router(tentativas_router)
    app.include_router(pagamentos_router)
    app.include_router(pdf_router)

    return app
