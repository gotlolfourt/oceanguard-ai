from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@localhost/oceanguard_db"
    REDIS_URL: str = "redis://localhost:6379/0"
    JWT_SECRET_KEY: str = "secret"
    CORS_ORIGINS: list = ["http://localhost:5173"]
    
    class Config:
        env_file = ".env"

settings = Settings()