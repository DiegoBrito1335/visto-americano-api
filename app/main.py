from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

# Routers
from app.routers.auth import router as auth_router
from app.routers.usuarios import router as usuarios_router
from app.routers.perguntas import router as perguntas_router
from app.routers.tentativas import router as tentativas_router
from app.routers.pagamentos import router as pagamentos_router
from app.routers.pdf import router as pdf_router


app = FastAPI(title=settings.APP_NAME)

# CORS — mantenha seguro em produção
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL,
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers (prefix sem /api — REST moderno)
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(usuarios_router, prefix="/usuarios", tags=["Usuários"])
app.include_router(perguntas_router, prefix="/perguntas", tags=["Perguntas"])
app.include_router(tentativas_router, prefix="/tentativas", tags=["Tentativas"])
app.include_router(pagamentos_router, prefix="/pagamentos", tags=["Pagamentos"])
app.include_router(pdf_router, prefix="/pdf", tags=["PDF"])


@app.get("/")
def root():
    return {"message": "API Visto Americano - OK"}


