from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.security import get_current_user
from app.services.usuarios_service import usuarios_service
from app.schemas.usuarios_schema import UsuarioCreate, UsuarioResponse
from app import models

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"]
)

# ================================
# REGISTRAR NOVO USUÁRIO
# ================================
@router.post("/registrar", response_model=UsuarioResponse, status_code=201)
def registrar(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    novo_usuario = usuarios_service.registrar(
        db=db,
        email=usuario.email,
        senha=usuario.senha
    )
    return novo_usuario


# ================================
# DADOS DO USUÁRIO LOGADO
# ================================
@router.get("/me", response_model=UsuarioResponse)
def me(current_user = Depends(get_current_user)):
    return current_user


# ================================
# LISTAR TODOS (APENAS AUTENTICADO, DEPOIS ADMIN)
# ================================
@router.get("/lista")
def listar_todos(
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user)  # protege a rota
):
    return usuarios_service.listar_todos(db)


# ================================
# TORNAR PREMIUM (APENAS AUTENTICADO, DEPOIS ADMIN)
# ================================
@router.post("/{usuario_id}/tornar-premium")
def tornar_premium(
    usuario_id: int,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user)  # protege a rota
):
    usuario_atualizado = usuarios_service.tornar_premium(db, usuario_id)

    return {
        "mensagem": "Usuário atualizado para Premium!",
        "usuario": {
            "id": usuario_atualizado.id,
            "email": usuario_atualizado.email,
            "plano": usuario_atualizado.tipo_plano
        }
    }
