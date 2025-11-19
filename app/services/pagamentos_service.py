# app/services/pagamentos_service.py
import os
from datetime import datetime, timedelta
from typing import Optional

import stripe
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app import models

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")


class PagamentosService:
    """
    Serviço para lidar com Stripe Checkout e ativação de plano Premium.
    """

    def __init__(self):
        # permite sobrescrever price_id via env
        self.default_price_id = os.getenv("STRIPE_PRICE_ID")

    def criar_checkout_session(
        self,
        customer_email: str,
        success_url: str,
        cancel_url: str,
        price_id: Optional[str] = None,
        quantity: int = 1,
    ) -> dict:
        """
        Cria uma sessão de checkout no Stripe e retorna a URL de checkout.
        """
        price = price_id or self.default_price_id
        if not price:
            raise HTTPException(
                status_code=500,
                detail="Nenhum price_id foi configurado (STRIPE_PRICE_ID) e nenhum price_id foi enviado."
            )

        try:
            session = stripe.checkout.Session.create(
                customer_email=customer_email,
                payment_method_types=["card"],
                mode="payment",
                line_items=[{"price": price, "quantity": quantity}],
                success_url=success_url,
                cancel_url=cancel_url,
            )
            return {"url": session.url, "id": session.id}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao criar sessão Stripe: {str(e)}")

    def ativar_premium_por_email(self, db: Session, email: str, dias: int = 365 * 1) -> models.Usuario:
        """
        Ativa o plano premium para um usuário identificado pelo email.
        Define data_expiracao_premium para 'dias' dias a partir de agora.
        """
        usuario = db.query(models.Usuario).filter(models.Usuario.email == email).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        usuario.tipo_plano = "premium"
        usuario.data_expiracao_premium = datetime.utcnow() + timedelta(days=dias)
        db.commit()
        db.refresh(usuario)
        return usuario

    def ativar_premium_por_id(self, db: Session, usuario_id: int, dias: int = 365 * 1) -> models.Usuario:
        usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        usuario.tipo_plano = "premium"
        usuario.data_expiracao_premium = datetime.utcnow() + timedelta(days=dias)
        db.commit()
        db.refresh(usuario)
        return usuario

    def processar_webhook(self, payload: bytes, sig_header: str, db: Session):
        """
        Valida e processa eventos do Stripe (p.ex. checkout.session.completed).
        Retorna dict com status e detalhes.
        """
        webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
        if not webhook_secret:
            raise HTTPException(status_code=500, detail="STRIPE_WEBHOOK_SECRET não configurado")

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
        except stripe.error.SignatureVerificationError as e:
            raise HTTPException(status_code=400, detail=f"Assinatura inválida: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Erro ao interpretar webhook: {str(e)}")

        # Processar tipos de evento que interessam
        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]  # tipo: dict
            # Obter o e-mail do cliente
            customer_email = (session.get("customer_details") or {}).get("email")
            # Em alguns setups o email fica em customer_email, tente também:
            if not customer_email:
                customer_email = session.get("customer_email")

            if customer_email:
                # Ativar premium (padrão 1 ano) -- ajustar conforme plano/metadata
                usuario = db.query(models.Usuario).filter(models.Usuario.email == customer_email).first()
                if usuario:
                    usuario.tipo_plano = "premium"
                    # se quiser usar metadata para dias:
                    dias = 365
                    # exemplo: if session.get("metadata") and session["metadata"].get("period_days"): ...
                    usuario.data_expiracao_premium = datetime.utcnow() + timedelta(days=dias)
                    db.commit()
                    return {"status": "ok", "mensagem": f"Usuário {customer_email} atualizado para premium via webhook."}
                else:
                    return {"status": "warning", "mensagem": "Pagamento recebido, mas usuário não encontrado."}
        # Retorne success para outros eventos ou não processados
        return {"status": "ignored", "tipo_evento": event["type"]}


# instância
pagamentos_service = PagamentosService()
