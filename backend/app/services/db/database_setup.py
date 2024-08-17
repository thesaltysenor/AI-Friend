# app/db/database_setup.py

import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = f"{settings.DATABASE_URL}?charset=utf8mb4"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=10,
    max_overflow=20,
    echo=False
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables() -> None:
    try:
        # Import all models to ensure they are registered
        from app.models.user import User
        from app.models.character import Character
        from app.models.messages import Message
        from app.models.image import GeneratedImage
        from app.models.conversation_intent import ConversationIntent
        from app.models.interaction import Interaction
        from app.models.entity import Entity
        from app.models.feedback import Feedback
        from app.models.session import Session
        from app.models.user_preference import UserPreference
        
        # This will create all tables
        Base.metadata.create_all(bind=engine)
        
        # Explicitly configure all mappers
        from sqlalchemy.orm import configure_mappers
        configure_mappers()
        
        logger.info("Database tables created and mappers configured successfully.")
    except Exception as e:
        logger.error(f"Error creating database tables or configuring mappers: {e}")
        raise

def init_db() -> None:
    try:
        # Test database connection
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        logger.info("Database connection successful.")
        
        create_tables()
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise