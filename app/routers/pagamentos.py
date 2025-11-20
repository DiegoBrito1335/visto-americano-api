# app/routers/pagamentos.py

from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional

from app.database import get_db
from app.core.security import get_current_user
from app.core.config import settings
from app.services.pagamentos_service import pagamentos_service
from app import models

router = APIRouter(
    prefix="/pagamentos",
    tags=["Pagamentos"]
)

# ======================================================
# MODELO DE REQUEST PARA CHECKOUT
# ======================================================

class CreateSessionRequest(BaseModel):
    success_url: str
    cancel_url: str
    price_id: Optional[str] = None
    quantity: int = 1
    email: Optional[EmailStr] = None


# ======================================================
# CRIAR CHECKOUT (CLIENTE)
# ======================================================

@router.post("/create-session")
def create_checkout_session(
    data: CreateSessionRequest,
    db: Session = Depends(get_db)
):
    """
    Cria uma sessão de checkout no Stripe.
    O frontend deve redirecionar o usuário para a URL retornada.
    """

    if not data.email:
        raise HTTPException(status_code=400, detail="Email é obrigatório para o checkout")

    # Carrega o preço do Stripe de forma centralizada (settings)
    price_id = data.price_id or settings.STRIPE_PRICE_ID

    if not price_id:
        raise HTTPException(status_code=500, detail="Stripe PRICE_ID não configurado")

    return pagamentos_service.criar_checkout_session(
        customer_email=data.email,
        success_url=data.success_url,
        cancel_url=data.cancel_url,
        price_id=price_id,
        quantity=data.quantity,
        db=db
    )


# ======================================================
# WEBHOOK DO STRIPE (PÚBLICO)
# ======================================================

@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Webhook — recebe eventos do Stripe.
    """

    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    if not sig_header:
        raise HTTPException(status_code=400, detail="Cabeçalho stripe-signature ausente")

    return pagamentos_service.processar_webhook(
        payload=payload,
        signature=sig_header,
        db=db
    )


# ======================================================
# ATIVAÇÃO MANUAL (ADMIN/DEBUG)
# ======================================================

@router.post("/ativar/{usuario_id}")
def ativar_manual(
    usuario_id: int,
    current_user: models.Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Ativa premium manualmente (somente para admin / testes).
    """

    # Exemplo para futuro:
    # if not current_user.is_admin:
    #    raise HTTPException(status_code=403, detail="Acesso negado")

    usuario = pagamentos_service.ativar_premium_por_id(db, usuario_id)

    return {
        "mensagem": "Usuário tornado premium manualmente.",
        "usuario": {
            "id": usuario.id,
            "email": usuario.email,
            "plano": usuario.tipo_plano
        }
    }
