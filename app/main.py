from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import auth, tentativas, usuarios, perguntas, pagamentos, pdf
from app.database import init_db

# ============================================================
#  CORS DEFINITIVO — domínio principal + Vercel + localhost
# ============================================================
def build_cors_list():
    origins = set()

    # Domínio principal do front
    if settings.FRONTEND_URL:
        base = settings.FRONTEND_URL.strip()
        origins.add(base)

        host = base.replace("https://", "").replace("http://", "")
        origins.add(f"https://{host}")
        origins.add(f"http://{host}")
        origins.add(f"https://www.{host}")
        origins.add(f"http://www.{host}")

    # Backend (caso front acesse diretamente)
    if settings.BACKEND_URL:
        origins.add(settings.BACKEND_URL.strip())

    # Local dev
    origins.add("http://localhost:3000")
    origins.add("http://127.0.0.1:3000")

    # Preview Vercel
    origins.add("https://visto-americano-api-git-main-diego-santos-de-brito-s-projects.vercel.app")

    print("🔐 ORIGENS LIBERADAS PELO CORS:", origins)

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

    # OPTIONS global — evita erro 400
    @app.options("/{rest_of_path:path}")
    async def options_handler(rest_of_path: str):
        return Response(status_code=200)

    # ROTAS
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
            "allowed_origins": allowed_origins,
            "environment": settings.ENVIRONMENT
        }

    return app


app = create_app()



