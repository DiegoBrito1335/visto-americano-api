from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import Usuario, UsuarioCreate
from app.services.usuarios_service import (
    criar_usuario,
    autenticar_usuario,
    gerar_token
)

router = APIRouter(prefix="/api", tags=["auth"])


@router.post("/registrar", response_model=Usuario)
def registrar(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_db = criar_usuario(db, usuario)
    return usuario_db


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    usuario = autenticar_usuario(db, form_data.username, form_data.password)

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = gerar_token(usuario)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "usuario": {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "premium": usuario.premium
        }
    }
