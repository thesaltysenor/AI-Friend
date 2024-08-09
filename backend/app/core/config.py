import logging
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '.env')
load_dotenv(dotenv_path)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug(f"Loading .env from {dotenv_path}")

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Friend API"
    API_V1_STR: str = "/api/v1"
    ALLOWED_ORIGINS: list = ["http://localhost:8081"]

    api_base_url: str = os.getenv("LM_STUDIO_API_URL", "http://localhost:1234/v1")
    MYSQL_HOSTNAME: str = os.getenv("MYSQL_HOSTNAME", "ai-friend-db")
    MYSQL_USER: str = os.getenv("MYSQL_USER", "root")
    MYSQL_ROOT_USER: str = os.getenv("MYSQL_ROOT_USER", "root")
    MYSQL_ROOT_PASSWORD: str = os.getenv("MYSQL_ROOT_PASSWORD", "letmein")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "letmein")
    MYSQL_DB: str = os.getenv("MYSQL_DB", "ai-friend-db")
    MYSQL_PORT: int = int(os.getenv("MYSQL_PORT", 3306))
    SECRET_KEY: str = os.getenv("SECRET_KEY", "b'uW\xf9{\xe3\xc3\xad\xc9[\xa1\xe0\xa5\x1d\xd1\x92\x02^-\x07\x9f=\xd3N\xe0\xaf\x92>f\xe5\xfc\xee#'")

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # ComfyUI settings
    COMFYUI_BASE_URL: str = os.getenv("COMFYUI_BASE_URL", "http://comfyui:8188")
    COMFYUI_CHECKPOINT: str = "v1-5-pruned.ckpt"
    COMFYUI_NEGATIVE_PROMPT: str = "bad, unrealistic"
    COMFYUI_STEPS: int = 20
    COMFYUI_CFG_SCALE: float = 8.0
    COMFYUI_WIDTH: int = 512
    COMFYUI_HEIGHT: int = 512
    COMFYUI_SEED: int = 5555
    COMFYUI_SAMPLER_NAME: str = "euler"
    COMFYUI_SCHEDULER: str = "normal"
    COMFYUI_DENOISE: float = 1.0
    COMFYUI_BATCH_SIZE: int = 1
    COMFYUI_FILENAME_PREFIX: str = "ComfyUI"
    
    class Config:
        env_file = ".env"
        extra = "allow"

    @property
    def DATABASE_URL(self):
        if os.getenv("RUNNING_IN_DOCKER") == "true":
            return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOSTNAME}:{self.MYSQL_PORT}/{self.MYSQL_DB}"
        else:
            # Use localhost and the mapped port when running locally
            return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@localhost:3320/{self.MYSQL_DB}"

settings = Settings()
logger.debug(f"Settings loaded: API_BASE_URL={settings.api_base_url}, DATABASE_URL={settings.DATABASE_URL}")