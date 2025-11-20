from datetime import datetime, timedelta
from jose import jwt, JWTError, ExpiredSignatureError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database import get_db
from app import models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ======================================================
# HASH DE SENHA
# ======================================================
# Configuração para usar tanto bcrypt quanto argon2
pwd_context = CryptContext(schemes=["bcrypt", "argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ======================================================
# GERAÇÃO DE TOKENS
# ======================================================
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow()
    })

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    expire = datetime.utcnow() + (expires_delta or timedelta(days=30))
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow()
    })

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


# ======================================================
# DECODIFICA TOKEN
# ======================================================
def decode_token(token: str):
    try:
        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")


# ======================================================
# EXTRAI TOKEN DA REQUEST (COOKIE OU BEARER)
# ======================================================
def get_token_from_request(request: Request) -> str | None:
    """
    Tenta obter token em:
    1. Cookie HttpOnly: access_token
    2. Authorization: Bearer <token>
    """

    # 1 — Cookie access_token (o correto)
    access_cookie = request.cookies.get("access_token")
    if access_cookie:
        return access_cookie

    # 2 — Header Authorization
    auth = request.headers.get("Authorization")
    if auth and auth.startswith("Bearer "):
        return auth.removeprefix("Bearer ")

    return None


# ======================================================
# OBTÉM USUÁRIO ATUAL A PARTIR DO TOKEN
# ======================================================
def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = get_token_from_request(request)

    if not token:
        raise HTTPException(status_code=401, detail="Não autenticado")

    payload = decode_token(token)

    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Token sem usuário")

    user = db.query(models.Usuario).filter(models.Usuario.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return user
