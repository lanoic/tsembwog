from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    CORS_ORIGINS: str = "*"
    class Config: env_file = ".env"
settings = Settings()
