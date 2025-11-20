# app/services/pagamentos_service.py

import stripe
from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.core.config import settings
from app import models
from app.services.usuarios_service import usuarios_service

# Configura a chave secreta do Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


class PagamentosService:

    # =====================================================
    # 1) CRIAR CHECKOUT SESSION
    # =====================================================
    def criar_checkout_session(
        self,
        customer_email: str,
        success_url: str,
        cancel_url: str,
        price_id: str,
        quantity: int = 1
    ):
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[{
                    "price": price_id,
                    "quantity": quantity
                }],
                mode="payment",
                customer_email=customer_email,
                success_url=success_url,
                cancel_url=cancel_url
            )
            return {"checkout_url": session.url}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao criar checkout: {str(e)}")

    # =====================================================
    # 2) PROCESSAR WEBHOOK DO STRIPE
    # =====================================================
    def processar_webhook(self, payload: bytes, sig_header: str, db: Session):
        try:
            evento = stripe.Webhook.construct_event(
                payload=payload,
                sig_header=sig_header,
                secret=settings.STRIPE_WEBHOOK_SECRET
            )
        except Exception:
            raise HTTPException(status_code=400, detail="Webhook inválido")

        # --------------------------
        # Pagamento concluído
        # --------------------------
        if evento["type"] == "checkout.session.completed":
            dados = evento["data"]["object"]

            email = dados.get("customer_email")
            if email:
                usuario = usuarios_service.buscar_por_email(db, email)
                if usuario:
                    usuario.tipo_plano = "premium"
                    usuario.data_expiracao_premium = datetime.utcnow() + timedelta(days=30)

                    db.commit()
                    db.refresh(usuario)

        return {"status": "ok"}

    # =====================================================
    # 3) ATIVAÇÃO MANUAL (ADMIN)
    # =====================================================
    def ativar_premium_por_id(self, db: Session, usuario_id: int):
        usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()

        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        usuario.tipo_plano = "premium"
        usuario.data_expiracao_premium = None  # vitalício

        db.commit()
        db.refresh(usuario)

        return usuario


# Instância padrão (igual outros services)
pagamentos_service = PagamentosService()
