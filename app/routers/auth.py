from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.database import get_db
from app.schemas import UsuarioCriar, UsuarioResposta, Token
from app.services.usuarios_service import criar_usuario, autenticar_usuario, gerar_token
from app.core.config import settings

router = APIRouter()

@router.post("/register", response_model=UsuarioResposta, status_code=status.HTTP_201_CREATED)
def register(usuario: UsuarioCriar, db: Session = Depends(get_db)):
    try:
        novo = criar_usuario(db, usuario)
        return novo
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = autenticar_usuario(db, form_data.username, form_data.password)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    access_token = gerar_token(usuario, expires_delta=timedelta(minutes=60))
    return {"access_token": access_token, "token_type": "bearer"}
