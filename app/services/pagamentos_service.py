from sqlalchemy.orm import Session
from app.models import Usuario

def ativar_premium(db: Session, user_id: int):
    user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not user:
        return None

    user.premium = True
    db.commit()
    db.refresh(user)
    return user
