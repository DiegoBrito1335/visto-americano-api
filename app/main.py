from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import auth, tentativas, usuarios, perguntas, pagamentos, pdf
from app.database import init_db


def build_cors_list():
    origins = set()

    # ORIGEM PRINCIPAL
    if settings.FRONTEND_URL:
        origins.add(settings.FRONTEND_URL.strip())

    # ORIGEM ADICIONAL (Railway/Vercel)
    if hasattr(settings, "CORS_ADDITIONAL_ORIGIN") and settings.CORS_ADDITIONAL_ORIGIN:
        origins.add(settings.CORS_ADDITIONAL_ORIGIN.strip())

    # WWW e sem www + HTTP/HTTPS
    generated = set()
    for origin in origins:
        base = origin.replace("https://", "").replace("http://", "")

        generated.add(f"https://{base}")
        generated.add(f"http://{base}")
        generated.add(f"https://www.{base}")
        generated.add(f"http://www.{base}")

    origins.update(generated)

    # Desenvolvimento
    origins.add("http://localhost:3000")
    origins.add("http://localhost:3001")
    origins.add("http://127.0.0.1:3000")

    # Preview Vercel
    origins.add("https://visto-americano-kvsqp896m-diego-santos-de-brito-s-projects.vercel.app")

    return list(origins)


def create_app():
    app = FastAPI(title=settings.APP_NAME)

    @app.on_event("startup")
    def startup_event():
        init_db()

    allowed_origins = build_cors_list()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ============================
    # HANDLER GLOBAL PARA OPTIONS
    # ============================
    @app.options("/{rest_of_path:path}")
    async def preflight_handler(rest_of_path: str):
        return Response(status_code=200)

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


