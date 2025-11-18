from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas import UsuarioResposta
from app.core.security import get_current_user
from app.services.usuarios_service import get_user_by_id, list_users, make_premium

router = APIRouter()

@router.get("/me", response_model=UsuarioResposta)
def me(current_user=Depends(get_current_user)):
    return current_user

@router.get("/", response_model=List[UsuarioResposta])
def list_all(db: Session = Depends(get_db)):
    # endpoint para admin/debug
    return list_users(db)

@router.post("/{usuario_id}/premium")
def tornar_premium(usuario_id: int, db: Session = Depends(get_db)):
    user = make_premium(db, usuario_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"message": "Usuário atualizado para premium", "user_id": user.id}
