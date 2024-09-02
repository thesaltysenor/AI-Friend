# ai-friend/backend/app/main.py
from app.core.exceptions import CharacterDatabaseException
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
import asyncio

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
        
async def download_nltk_data():
    loop = asyncio.get_event_loop()
    try:
        await loop.run_in_executor(None, nltk.download, 'stopwords')
    except Exception as e:
        logger.error(f"NLTK data download failed: {e}")
        raise

async def initialize_database():
    init_db()

async def populate_characters():
    try:
        db = next(get_db())
        character_database = CharacterDatabase(db)
        character_database.populate_characters()
        character_database.get_or_create_default_character()
    except CharacterDatabaseException as e:
        logger.error(f"Failed to populate characters: {e}")
        raise
    finally:
        db.close()

async def connect_external_services():
    comfy_ui_service = get_comfy_ui_service()
    await comfy_ui_service.connect()
    await start_background_tasks(context_manager)

async def startup_tasks():
    await initialize_database()
    await populate_characters()
    await connect_external_services()
    await download_nltk_data()

async def shutdown_tasks():
    try:
        await context_manager.shutdown()
        comfy_ui_service = get_comfy_ui_service()
        await comfy_ui_service.disconnect()
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")
    finally:
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