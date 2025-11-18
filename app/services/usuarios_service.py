from sqlalchemy.orm import Session
from datetime import timedelta
from app import models
from app.schemas import UsuarioCreate
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.config import settings

def get_user_by_email(db: Session, email: str):
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.Usuario).filter(models.Usuario.id == user_id).first()

def criar_usuario(db: Session, usuario: UsuarioCreate):
    existente = get_user_by_email(db, usuario.email)
    if existente:
        raise ValueError("Email já cadastrado")
    hashed = get_password_hash(usuario.senha)
    novo = models.Usuario(
        nome_completo=usuario.nome_completo,
        email=usuario.email,
        senha_hash=hashed,
        tipo_plano="gratuito",
        ativo=True
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

def autenticar_usuario(db: Session, email: str, senha: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(senha, user.senha_hash):
        return None
    return user

def gerar_token(usuario, expires_delta: timedelta | None = None):
    data = {"sub": usuario.email}
    return create_access_token(data, expires_delta)

def list_users(db: Session):
    users = db.query(models.Usuario).all()
    return users

def make_premium(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    user.tipo_plano = "premium"
    user.data_expiracao_premium = None
    db.commit()
    db.refresh(user)
    return user
