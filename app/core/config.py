from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ======================================================
    # INFORMAÇÕES GERAIS
    # ======================================================
    APP_NAME: str = "Visto Americano API"

    # ======================================================
    # JWT
    # ======================================================
    SECRET_KEY: str                  # Obrigatório no .env
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # ======================================================
    # BANCO DE DADOS
    # ======================================================
    # Fallback SQLite para ambiente local
    DATABASE_URL: str = "sqlite:///./local.db"

    # ======================================================
    # STRIPE
    # ======================================================
    STRIPE_SECRET_KEY: str = ""
    STRIPE_PUBLISHABLE_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    STRIPE_PRICE_ID: str = ""

    # ======================================================
    # PAGAMENTO INTERNO
    # ======================================================
    PRECO_PREMIUM: int = 7990  # Em centavos (R$ 79,90)

    # ======================================================
    # AMBIENTE
    # ======================================================
    ENVIRONMENT: str = "development"  # development | production

    # ======================================================
    # URLs DO SISTEMA
    # ======================================================
    FRONTEND_URL: str = "http://localhost:3000"
    BACKEND_URL: str = "http://localhost:8000"

    class Config:
        env_file = ".env"
        extra = "allow"  # Permite variáveis adicionais no .env sem erro

    # ------------------------------------------------------
    # PROPRIEDADES PARA COMPATIBILIDADE (opcional)
    # ------------------------------------------------------
    @property
    def JWT_SECRET(self):
        return self.SECRET_KEY

    @property
    def JWT_ALGORITHM(self):
        return self.ALGORITHM


settings = Settings()
