import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import ai_personality
from app.core.config import settings
from app.services.chat.context_manager import ChatContextManager
from app.services.background_tasks import start_background_tasks
from contextlib import asynccontextmanager
from app.services.db.session import engine
from app.services.db.base import Base
import nltk
from app.api.v1.endpoints import auth, chat, models, image_generation
from app.services.db.ai_personality_manager import AIPersonalityManager
from app.services.ai.comfy_ui_service import ComfyUIService

try:
    nltk.data.find('stopwords')
except LookupError:
    nltk.download('stopwords')

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

context_manager = ChatContextManager()
comfy_ui_service = ComfyUIService(base_url=settings.COMFYUI_BASE_URL)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.debug("Starting application lifespan.")
    # Create database tables
    try:
        Base.metadata.create_all(bind=engine)
        logger.debug("Tables created successfully.")
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
    
    # Populate characters
    try:
        ai_personality_manager = AIPersonalityManager()
        ai_personality_manager.populate_characters()
        ai_personality_manager.get_or_create_default_ai_personality()
        logger.debug("Characters populated successfully.")
    except Exception as e:
        logger.error(f"Error during startup: {e}")
    
    # Connect to ComfyUI
    try:
        await comfy_ui_service.connect()
        logger.debug("Connected to ComfyUI successfully.")
    except Exception as e:
        logger.error(f"Error connecting to ComfyUI: {e}")
    
    # Startup code
    await start_background_tasks(context_manager)
    
    yield
    
    # Shutdown code
    await context_manager.shutdown()
    
    # Disconnect from ComfyUI
    try:
        await comfy_ui_service.disconnect()
        logger.debug("Disconnected from ComfyUI successfully.")
    except Exception as e:
        logger.error(f"Error disconnecting from ComfyUI: {e}")
    
    logger.debug("Shutting down application lifespan.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(chat.router, prefix=f"{settings.API_V1_STR}/chat", tags=["chat"])
app.include_router(models.router, prefix=f"{settings.API_V1_STR}/models", tags=["models"])
app.include_router(ai_personality.router, prefix=f"{settings.API_V1_STR}/ai_personalities", tags=["ai_personalities"])
app.include_router(image_generation.router, prefix=f"{settings.API_V1_STR}/image", tags=["image"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)