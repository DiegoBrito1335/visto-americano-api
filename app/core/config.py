from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str
    ENVIRONMENT: str
    FRONTEND_URL: str
    BACKEND_URL: str

    DATABASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    PRECO_PREMIUM: int

    STRIPE_SECRET_KEY: str
    STRIPE_PUBLISHABLE_KEY: str
    STRIPE_WEBHOOK_SECRET: str
    STRIPE_PRICE_ID: str

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
