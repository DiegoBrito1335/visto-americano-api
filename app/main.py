from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import auth, tentativas, usuarios, perguntas, pagamentos, pdf
from app.database import init_db


# ============================================================
#  CORS DINÂMICO — aceita domínio principal, Vercel e localhost
# ============================================================
def build_cors_list():
    origins = set()

    # ORIGEM PRINCIPAL
    if settings.FRONTEND_URL:
        base = settings.FRONTEND_URL.strip()
        origins.add(base)

        # versão sem http/https
        host = base.replace("https://", "").replace("http://", "")
        origins.add(f"https://{host}")
        origins.add(f"http://{host}")
        origins.add(f"https://www.{host}")
        origins.add(f"http://www.{host}")

    # BACKEND_URL como permitido (caso front faça preview)
    if settings.BACKEND_URL:
        origins.add(settings.BACKEND_URL.strip())

    # localhost (DEV)
    origins.add("http://localhost:3000")
    origins.add("http://127.0.0.1:3000")

    # Preview Vercel
    origins.add("https://visto-americano-api-git-main-diego-santos-de-brito-s-projects.vercel.app")

    print("🔐 ORIGENS LIBERADAS PELO CORS:", origins)

    return list(origins)


# ============================================================
#  CRIAÇÃO DO APP FASTAPI
# ============================================================
def create_app():
    app = FastAPI(title=settings.APP_NAME)

    @app.on_event("startup")
    def startup_event():
        init_db()

    allowed_origins = build_cors_list()

    # Middleware CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ROTAS
    app.include_router(auth.router)
    app.include_router(usuarios.router)
    app.include_router(perguntas.router)
    app.include_router(tentativas.router)
    app.include_router(pagamentos.router)
    app.include_router(pdf.router)

    # HEALTHCHECK
    @app.get("/")
    def root():
        return {
            "status": "online",
            "allowed_origins": allowed_origins,
            "environment": settings.ENVIRONMENT
        }

    return app


app = create_app()



