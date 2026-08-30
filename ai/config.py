from pydantic_settings import BaseSettings

class AISettings(BaseSettings):
    MODEL_PATH: str = "/models"
    YOLO_MODEL_NAME: str = "yolov8n"
    YOLO_CONFIDENCE_THRESHOLD: float = 0.5
    REDIS_URL: str = "redis://localhost:6379/0"
    
    class Config:
        env_file = ".env"

settings = AISettings()