from pydantic_settings import BaseSettings, SettingsConfigDict


class AISettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    MODEL_PATH: str = "/models"
    YOLO_MODEL_NAME: str = "yolov8n"
    YOLO_CONFIDENCE_THRESHOLD: float = 0.5
    REDIS_URL: str = "redis://localhost:6379/0"
    USE_MOCK_MODE: bool = True


settings = AISettings()
