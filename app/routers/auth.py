from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth_schema import LoginSchema
from app.core.security import (
    create_access_token,
    create_refresh_token
)
from app.core.config import settings
from app.services.usuarios_service import usuarios_service

router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"]
)

# OPTIONS fix — evita erro 400 no preflight
@router.options("/login")
def options_login():
    return Response(status_code=200)

@router.post("/login")
def login(data: LoginSchema, response: Response, db: Session = Depends(get_db)):
    usuario = usuarios_service.autenticar(db, data.email, data.senha)

    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    access_token = create_access_token({"sub": usuario.email})
    refresh_token = create_refresh_token({"sub": usuario.email})

    is_prod = settings.ENVIRONMENT == "production"

    # Cookies cross-site (Vercel → Railway)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=is_prod,
        samesite="None" if is_prod else "Lax",
        path="/"
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=is_prod,
        samesite="None" if is_prod else "Lax",
        path="/"
    )

    return {
        "mensagem": "Login efetuado com sucesso",
        "usuario": {
            "id": usuario.id,
            "email": usuario.email
        },
        "access_token": access_token
    }

