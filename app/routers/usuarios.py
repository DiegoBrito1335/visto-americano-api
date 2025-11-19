from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from app.database import get_db
from app.schemas import UsuarioCriar, UsuarioLogin, UsuarioResposta, Token
from app.core.security import create_access_token
from app.services.usuarios_service import usuarios_service
from app.core.security import get_current_user



router = APIRouter(tags=["Usuários"])  # prefix definido no main.py


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
# LOGIN
# ================================
@router.post("/login", response_model=Token)
def login(dados: UsuarioLogin, db: Session = Depends(get_db)):
    usuario = usuarios_service.autenticar(
        db=db,
        email=dados.email,
        senha=dados.senha,
    )

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": usuario.email},
        expires_delta=timedelta(minutes=60)
    )

    return {"access_token": access_token, "token_type": "bearer"}


# ================================
# USUÁRIO LOGADO
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
