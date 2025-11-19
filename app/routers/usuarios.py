from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from app.database import get_db
from app.schemas import UsuarioCriar, UsuarioResposta
from app.core.security import get_current_user
from app.services.usuarios_service import usuarios_service

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"]
)

# ================================
# REGISTRAR NOVO USUÁRIO
# ================================
@router.post("/registrar", response_model=UsuarioResposta, status_code=201)
def registrar(usuario: UsuarioCriar, db: Session = Depends(get_db)):
    novo_usuario = usuarios_service.registrar(
        db=db,
        email=usuario.email,
        senha=usuario.senha,
        nome=usuario.nome_completo,
    )
    return novo_usuario


# ================================
# DADOS DO USUÁRIO LOGADO
# ================================
@router.get("/me", response_model=UsuarioResposta)
def me(current_user=Depends(get_current_user)):
    return current_user


# ================================
# LISTAR TODOS (ADMIN)
# ================================
@router.get("/lista")
def listar_todos(db: Session = Depends(get_db)):
    """Lista todos os usuários (somente para debug/admin)."""
    return usuarios_service.listar_todos(db)


# ================================
# TORNAR PREMIUM (ADMIN)
# ================================
@router.post("/{usuario_id}/tornar-premium")
def tornar_premium(usuario_id: int, db: Session = Depends(get_db)):
    usuario = usuarios_service.tornar_premium(db, usuario_id)

    return {
        "mensagem": "Usuário atualizado para Premium!",
        "usuario": {
            "id": usuario.id,
            "email": usuario.email,
            "plano": usuario.tipo_plano
        }
    }
