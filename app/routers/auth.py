from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta

from app.database import get_db
from app.core.security import create_access_token, verify_password
from app.services.usuarios_service import usuarios_service
from app.schemas import UsuarioLogin, UsuarioResposta, Token

router = APIRouter()

@router.post("/login", response_model=Token)
def login(dados: UsuarioLogin, db: Session = Depends(get_db)):

    usuario = usuarios_service.autenticar(db, dados.email, dados.senha)

    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = create_access_token(
        data={"sub": usuario.email},
        expires_delta=timedelta(minutes=60)
    )

    return {"access_token": token, "token_type": "bearer"}
