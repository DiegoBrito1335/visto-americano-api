from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import auth, usuarios, perguntas, tentativas, pagamentos, pdf

app = FastAPI(title=settings.APP_NAME)

# CORS: mantenha seguro em produção (use settings.FRONTEND_URL)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers (prefix sem /api, estilo REST profissional)
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuários"])
app.include_router(perguntas.router, prefix="/perguntas", tags=["Perguntas"])
app.include_router(tentativas.router, prefix="/tentativas", tags=["Tentativas"])
app.include_router(pagamentos.router, prefix="/pagamentos", tags=["Pagamentos"])
app.include_router(pdf.router, prefix="/pdf", tags=["PDF"])

@app.get("/")
def root():
    return {"message": "API Visto Americano - OK"}

