from sqlalchemy.orm import Session
from app import models

def ativar_premium(db: Session, user_id: int):
    user = db.query(models.Usuario).filter(models.Usuario.id == user_id).first()
    if not user:
        return None
    user.tipo_plano = "premium"
    user.data_expiracao_premium = None
    db.commit()
    db.refresh(user)
    return user
