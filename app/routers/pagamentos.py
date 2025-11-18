# app/pagamentos.py
"""
Sistema de Pagamentos com Stripe
Suporta: Cartão de Crédito + PIX
Modelo: Pagamento Único R$ 79,90
"""

import stripe
import os
from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.database import get_db
from app.models import Usuario
from app.auth import get_current_user
from pydantic import BaseModel
from typing import Optional

# Configuração do Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
PRECO_PREMIUM = 7990  # R$ 79,90 em centavos

router = APIRouter(prefix="/api/pagamentos", tags=["Pagamentos"])


class CheckoutRequest(BaseModel):
    metodo_pagamento: str  # "cartao" ou "pix"
    success_url: str
    cancel_url: str


class CheckoutResponse(BaseModel):
    checkout_url: Optional[str] = None
    session_id: Optional[str] = None
    pix_code: Optional[str] = None
    pix_qr_code: Optional[str] = None


@router.post("/criar-checkout", response_model=CheckoutResponse)
async def criar_checkout(
    dados: CheckoutRequest,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cria sessão de checkout do Stripe
    Suporta cartão de crédito e PIX
    """
    
    # Verificar se usuário já é premium
    if usuario.tipo_plano == "premium":
        raise HTTPException(status_code=400, detail="Você já é Premium!")
    
    try:
        # Criar sessão de checkout
        if dados.metodo_pagamento == "cartao":
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'brl',
                        'unit_amount': PRECO_PREMIUM,
                        'product_data': {
                            'name': 'Visto Americano - Premium',
                            'description': '90 perguntas + PDF + Email + Histórico + Suporte',
                            'images': ['https://seu-site.com/logo.png'],  # Adicione seu logo
                        },
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=dados.success_url + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=dados.cancel_url,
                client_reference_id=str(usuario.id),
                customer_email=usuario.email,
                metadata={
                    'usuario_id': str(usuario.id),
                    'tipo_upgrade': 'premium',
                }
            )
            
            return CheckoutResponse(
                checkout_url=session.url,
                session_id=session.id
            )
            
        elif dados.metodo_pagamento == "pix":
            # Criar Payment Intent para PIX
            payment_intent = stripe.PaymentIntent.create(
                amount=PRECO_PREMIUM,
                currency='brl',
                payment_method_types=['pix'],
                metadata={
                    'usuario_id': str(usuario.id),
                    'tipo_upgrade': 'premium',
                },
                receipt_email=usuario.email,
            )
            
            # Confirmar o Payment Intent para gerar o código PIX
            confirmed_intent = stripe.PaymentIntent.confirm(
                payment_intent.id,
                payment_method_data={
                    'type': 'pix',
                }
            )
            
            # Extrair código PIX
            pix_data = confirmed_intent.next_action.pix_display_qr_code
            
            return CheckoutResponse(
                pix_code=pix_data.data,
                pix_qr_code=pix_data.image_url_png,
                session_id=payment_intent.id
            )
        
        else:
            raise HTTPException(status_code=400, detail="Método de pagamento inválido")
            
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=f"Erro no Stripe: {str(e)}")


@router.get("/verificar-pagamento/{session_id}")
async def verificar_pagamento(
    session_id: str,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Verifica se o pagamento foi aprovado
    """
    try:
        # Verificar sessão de checkout
        if session_id.startswith("cs_"):
            session = stripe.checkout.Session.retrieve(session_id)
            status = session.payment_status
        else:
            # Payment Intent (PIX)
            payment_intent = stripe.PaymentIntent.retrieve(session_id)
            status = payment_intent.status
        
        return {
            "status": status,
            "pago": status in ["paid", "succeeded"],
            "usuario_premium": usuario.tipo_plano == "premium"
        }
        
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=f"Erro ao verificar: {str(e)}")


@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Webhook do Stripe para processar pagamentos
    Ativa Premium automaticamente quando pagamento confirmado
    """
    
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Payload inválido")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Assinatura inválida")
    
    # Processar eventos
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        usuario_id = int(session['client_reference_id'])
        
        # Ativar Premium
        ativar_premium(db, usuario_id)
        
    elif event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        usuario_id = int(payment_intent['metadata']['usuario_id'])
        
        # Ativar Premium (PIX confirmado)
        ativar_premium(db, usuario_id)
    
    return {"status": "success"}


def ativar_premium(db: Session, usuario_id: int):
    """
    Ativa plano Premium para o usuário
    """
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    
    if usuario:
        usuario.tipo_plano = "premium"
        usuario.data_expiracao_premium = None  # Vitalício
        db.commit()
        
        # Aqui você pode enviar email de confirmação
        # enviar_email_premium(usuario.email, usuario.nome_completo)


@router.get("/status")
async def status_pagamento(usuario: Usuario = Depends(get_current_user)):
    """
    Retorna status do plano do usuário
    """
    return {
        "plano": usuario.tipo_plano,
        "premium": usuario.tipo_plano == "premium",
        "data_expiracao": usuario.data_expiracao_premium,
        "vitalicio": usuario.data_expiracao_premium is None and usuario.tipo_plano == "premium"
    }
