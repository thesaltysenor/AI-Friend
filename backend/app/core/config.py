import logging
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os
from typing import List

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '.env')
load_dotenv(dotenv_path)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"Loading .env from {dotenv_path}")

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Friend API"
    API_V1_STR: str = "/api/v1"
    ALLOWED_ORIGINS: List[str] = ["http://localhost:8081"]

    API_BASE_URL: str = os.getenv("LM_STUDIO_API_URL", "http://localhost:1234/v1")
    API_BASE_URL_DOCKER: str = os.getenv("API_BASE_URL_DOCKER", "http://host.docker.internal:1234/v1")
    
    # Database settings
    MYSQL_HOSTNAME: str = os.getenv("MYSQL_HOSTNAME", "ai-friend-db")
    MYSQL_USER: str = os.getenv("MYSQL_USER", "root")
    MYSQL_ROOT_USER: str = os.getenv("MYSQL_ROOT_USER", "root")
    MYSQL_ROOT_PASSWORD: str = os.getenv("MYSQL_ROOT_PASSWORD", "letmein")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "letmein")
    MYSQL_DB: str = os.getenv("MYSQL_DB", "ai-friend-db")
    MYSQL_PORT: int = int(os.getenv("MYSQL_PORT", 3306))
    
    # Security settings
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # ComfyUI settings
    COMFYUI_BASE_URL: str = os.getenv("COMFYUI_BASE_URL", "http://comfyui:8188")
    COMFYUI_CHECKPOINT: str = os.getenv("COMFYUI_CHECKPOINT", "v1-5-pruned.ckpt")
    COMFYUI_NEGATIVE_PROMPT: str = os.getenv("COMFYUI_NEGATIVE_PROMPT", "bad, unrealistic")
    COMFYUI_STEPS: int = int(os.getenv("COMFYUI_STEPS", 20))
    COMFYUI_CFG_SCALE: float = float(os.getenv("COMFYUI_CFG_SCALE", 8.0))
    COMFYUI_WIDTH: int = int(os.getenv("COMFYUI_WIDTH", 512))
    COMFYUI_HEIGHT: int = int(os.getenv("COMFYUI_HEIGHT", 512))
    COMFYUI_SEED: int = int(os.getenv("COMFYUI_SEED", 5555))
    COMFYUI_SAMPLER_NAME: str = os.getenv("COMFYUI_SAMPLER_NAME", "euler")
    COMFYUI_SCHEDULER: str = os.getenv("COMFYUI_SCHEDULER", "normal")
    COMFYUI_DENOISE: float = float(os.getenv("COMFYUI_DENOISE", 1.0))
    COMFYUI_BATCH_SIZE: int = int(os.getenv("COMFYUI_BATCH_SIZE", 1))
    COMFYUI_FILENAME_PREFIX: str = os.getenv("COMFYUI_FILENAME_PREFIX", "ComfyUI")

    class Config:
        env_file = ".env"
        extra = "allow"

    @property
    def DATABASE_URL(self) -> str:
        if os.getenv("RUNNING_IN_DOCKER") == "true":
            return os.getenv("DATABASE_URL_DOCKER", "")
        else:
            return os.getenv("DATABASE_URL", f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@localhost:3320/{self.MYSQL_DB}")

    @property
    def CURRENT_API_BASE_URL(self) -> str:
        return self.API_BASE_URL_DOCKER if os.getenv("RUNNING_IN_DOCKER") == "true" else self.API_BASE_URL

settings = Settings()
logger.info(f"Settings loaded: API_BASE_URL={settings.CURRENT_API_BASE_URL}, DATABASE_URL={settings.DATABASE_URL}")