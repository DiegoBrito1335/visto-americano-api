from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.pagamentos_service import ativar_premium
from app.auth import get_current_user

router = APIRouter(
    prefix="/api/pagamentos",
    tags=["Pagamentos"]
)

@router.post("/ativar")
def ativar_premium_route(user_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user = ativar_premium(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    return {"message": "Premium ativado com sucesso!", "user_id": user.id}
