# app/models/__init__.py

# First, import Base to ensure it's available for all models
from app.services.db.database_setup import Base

# Then import all your models
from .base import BaseModel
from .user import User
from .character import Character
from .messages import Message
from .conversation_intent import ConversationIntent
from .interaction import Interaction
from .entity import Entity
from .feedback import Feedback
from .session import Session
from .user_preference import UserPreference
from .image import GeneratedImage

def init_models():
    # This function doesn't need to do anything, 
    # just importing it will register all models with Base.metadata
    pass

# This ensures all models are registered with Base.metadata
__all__ = [
    "Base",  # Add Base to __all__
    "BaseModel",
    "User",
    "Character",
    "Message",
    "GeneratedImage",
    "ConversationIntent",
    "Interaction",
    "Entity",
    "Feedback",
    "Session",
    "UserPreference",
    "init_models"
]