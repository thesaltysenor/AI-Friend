# ai-friend/backend/app/main.py

import logging
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.api.v1 import api_router
from app.core.config import settings
from app.services.chat.context_manager import ChatContextManager
from app.services.background_tasks import start_background_tasks
from contextlib import asynccontextmanager
from app.services.db.database_setup import init_db, get_db
from app.services.db.character_database import CharacterDatabase
from app.core.dependencies import get_comfy_ui_service
import nltk

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

context_manager = ChatContextManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.debug("Starting application lifespan.")
    try:
        await startup_tasks()
        yield
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise
    finally:
        await shutdown_tasks()

async def startup_tasks():
    # Initialize the database
    init_db()
    
    # Populate characters
    try:
        db = next(get_db())
        character_database = CharacterDatabase(db)
        character_database.populate_characters()
        character_database.get_or_create_default_character()
    except Exception as e:
        logger.error(f"Failed to populate characters: {e}")
        raise
    finally:
        db.close()
    
    comfy_ui_service = get_comfy_ui_service()
    await comfy_ui_service.connect()
    await start_background_tasks(context_manager)

    # Ensure NLTK data is downloaded
    try:
        nltk.data.find('stopwords')
    except LookupError:
        nltk.download('stopwords')

async def shutdown_tasks():
    await context_manager.shutdown()
    comfy_ui_service = get_comfy_ui_service()
    await comfy_ui_service.disconnect()
    logger.debug("Shutting down application lifespan.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)