"""
Configurações da aplicação
"""
import os
from typing import Optional


class Settings:
    """Configurações da aplicação"""
    
    # ============================================
    # APLICAÇÃO
    # ============================================
    APP_NAME: str = "Aprova Visto Americano API"
    VERSION: str = "1.0.0"
    
    # ============================================
    # BANCO DE DADOS
    # ============================================
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        os.getenv("URL_DO_BANCO_DE_DADOS", "sqlite:///./visto_local.db")
    )
    
    # ============================================
    # JWT / Segurança
    # ============================================
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        os.getenv("CHAVE_SECRETA", "sua-chave-secreta-aqui")
    )
    
    ALGORITHM: str = os.getenv(
        "ALGORITHM",
        os.getenv("ALGORITMO", "HS256")
    )
    
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        os.getenv("MINUTOS_EXPIRACAO_TOKEN", "30")
    ))
    
    # ============================================
    # STRIPE - PAGAMENTOS
    # ============================================
    STRIPE_SECRET_KEY: str = os.getenv(
        "STRIPE_SECRET_KEY",
        os.getenv("CHAVE_SECRETA_STRIPE", "")
    )
    
    STRIPE_PUBLISHABLE_KEY: str = os.getenv(
        "STRIPE_PUBLISHABLE_KEY",
        os.getenv("CHAVE_PUBLICA_STRIPE", "")
    )
    
    STRIPE_WEBHOOK_SECRET: str = os.getenv(
        "STRIPE_WEBHOOK_SECRET",
        os.getenv("SEGREDO_WEBHOOK_STRIPE", "")
    )
    
    STRIPE_PRICE_ID: str = os.getenv(
        "STRIPE_PRICE_ID",
        os.getenv("ID_PRECO_STRIPE", "")
    )
    
    PRECO_PREMIUM: int = int(os.getenv(
        "PRECO_PREMIUM",
        "7990"
    ))
    
    # ============================================
    # URLs
    # ============================================
    FRONTEND_URL: str = os.getenv(
        "FRONTEND_URL",
        os.getenv("URL_FRONTEND", "http://localhost:3000")
    )
    
    BACKEND_URL: str = os.getenv(
        "BACKEND_URL",
        os.getenv("URL_DE_ACKEND", "http://localhost:8000")
    )
    
    # ============================================
    # CORS - Origens permitidas
    # ============================================
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://aprovavistoamericano.com.br",
        "https://www.aprovavistoamericano.com.br",
    ]


# Instância única de configurações
settings = Settings()