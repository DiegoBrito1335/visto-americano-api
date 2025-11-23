from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import auth, tentativas, usuarios, perguntas, pagamentos, pdf
from app.database import init_db


def create_app():
    app = FastAPI(title=settings.APP_NAME)

    @app.on_event("startup")
    def startup_event():
        init_db()

    allowed_origins = [
        settings.FRONTEND_URL,
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

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


