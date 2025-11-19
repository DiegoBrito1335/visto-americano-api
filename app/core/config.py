from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Informações gerais
    APP_NAME: str = "Visto Americano API"

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Banco de dados
    DATABASE_URL: str

    # Stripe
    STRIPE_SECRET_KEY: str
    STRIPE_PUBLISHABLE_KEY: str
    STRIPE_WEBHOOK_SECRET: str
    STRIPE_PRICE_ID: str

    # Pagamento interno
    PRECO_PREMIUM: int = 7990  # centavos

    # Ambiente
    ENVIRONMENT: str = "development"

    # URLs
    FRONTEND_URL: str
    BACKEND_URL: str

    class Config:
        env_file = ".env"
        extra = "allow"  # <-- permite futuras variáveis sem quebrar


settings = Settings()
