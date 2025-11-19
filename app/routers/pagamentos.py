# app/routers/pagamentos.py
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
import os

from app.database import get_db
from app.core.security import get_current_user
from app.services.pagamentos_service import pagamentos_service
from app import models

router = APIRouter()


class CreateSessionRequest(BaseModel):
    success_url: str
    cancel_url: str
    price_id: str | None = None
    quantity: int = 1
    email: EmailStr | None = None  # se informado, prioriza este email


@router.post("/create-session")
def create_checkout_session(data: CreateSessionRequest, db: Session = Depends(get_db)):
    """
    Cria uma sessão de Checkout no Stripe.
    O frontend deve redirecionar o usuário para a URL retornada.
    """
    # decisão: permitir criar sessão sem token (frontend pode enviar email)
    email = data.email
    if not email:
        raise HTTPException(status_code=400, detail="Email do cliente é obrigatório")

    price_id = data.price_id or os.getenv("STRIPE_PRICE_ID")
    res = pagamentos_service.criar_checkout_session(
        customer_email=email,
        success_url=data.success_url,
        cancel_url=data.cancel_url,
        price_id=price_id,
        quantity=data.quantity
    )
    return res

@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Rota pública para o Stripe enviar eventos.
    Valida assinatura e processa o evento.
    """
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    if not sig_header:
        raise HTTPException(status_code=400, detail="Cabeçalho stripe-signature ausente")

    return pagamentos_service.processar_webhook(payload, sig_header, db)


@router.post("/ativar/{usuario_id}")
def ativar_manual(usuario_id: int, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    """
    Ativa premium manualmente (rota protegida).
    Útil para testes/admin.
    """
    # aqui você pode checar se current_user é admin (se tiver campo)
    usuario = pagamentos_service.ativar_premium_por_id(db, usuario_id)
    return {
        "mensagem": "Usuário tornado premium (manual).",
        "usuario": {"id": usuario.id, "email": usuario.email, "plano": usuario.tipo_plano}
    }
