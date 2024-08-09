from app.services.db.database import Base
from .user import User
from .ai_personality import AIPersonality
from .messages import Message
from .intent import Intent
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
__all__ = ["Base", "User", "AIPersonality", "Message", "GeneratedImage", "Intent", "Interaction", "Entity", "Feedback", "Session", "UserPreference", "init_models"]