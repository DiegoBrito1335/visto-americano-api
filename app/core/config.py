from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Visto Americano API"
    API_V1_STR: str = "/api"
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 dias
    FRONTEND_URL: str = "https://visto-americano-api.vercel.app"

    class Config:
        env_file = ".env"

settings = Settings()
