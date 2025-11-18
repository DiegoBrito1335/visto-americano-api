from sqlalchemy.orm import Session
from app.models import Usuario
from app.auth import gerar_hash_senha, verificar_senha


def get_user_by_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(Usuario).filter(Usuario.id == user_id).first()


def create_user(db: Session, email: str, password: str):
    hashed_password = gerar_hash_senha(password)
    user = Usuario(email=email, senha=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def validate_user_credentials(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    
    if not verificar_senha(password, user.senha):
        return None

    return user
