from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app import models
from app.schemas import UsuarioCreate
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY", "sua-chave-secreta-super-segura")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


def verificar_senha(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def gerar_hash_senha(senha: str) -> str:
    return pwd_context.hash(senha)


def gerar_token(usuario):
    dados = {"sub": usuario.email}
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dados.update({"exp": expire})
    return jwt.encode(dados, SECRET_KEY, algorithm=ALGORITHM)


def criar_usuario(db: Session, usuario: UsuarioCreate):
    existente = db.query(models.Usuario).filter(
        models.Usuario.email == usuario.email
    ).first()

    if existente:
        raise ValueError("Email já cadastrado")

    hashed = gerar_hash_senha(usuario.senha)

    novo = models.Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=hashed
    )

    db.add(novo)
    db.commit()
    db.refresh(novo)

    return novo


def autenticar_usuario(db: Session, email: str, senha: str):
    usuario = db.query(models.Usuario).filter(
        models.Usuario.email == email
    ).first()

    if not usuario:
        return None

    if not verificar_senha(senha, usuario.senha_hash):
        return None

    return usuario
