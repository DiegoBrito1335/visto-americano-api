auth_content = '''from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app import models, schemas
from app.database import get_db
import os

router = APIRouter(prefix="/api", tags=["auth"])

# Configurações
SECRET_KEY = os.getenv("SECRET_KEY", "sua-chave-secreta-super-segura")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/registrar", response_model=schemas.Usuario)
def registrar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    """Registra um novo usuário"""
    # Verifica se email já existe
    db_usuario = db.query(models.Usuario).filter(
        models.Usuario.email == usuario.email
    ).first()
    
    if db_usuario:
        raise HTTPException(
            status_code=400,
            detail="Email já cadastrado"
        )
    
    # Cria novo usuário
    hashed_password = get_password_hash(usuario.senha)
    novo_usuario = models.Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=hashed_password
    )
    
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    
    return novo_usuario


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Faz login e retorna token JWT"""
    usuario = db.query(models.Usuario).filter(
        models.Usuario.email == form_data.username
    ).first()
    
    if not usuario or not verify_password(form_data.password, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": usuario.email})
    
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
'''

with open("app/routers/auth.py", "w", encoding="utf-8") as f:
    f.write(auth_content)

print("✅ Criado: app/routers/auth.py")