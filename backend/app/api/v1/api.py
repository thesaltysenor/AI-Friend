# app/api/v1/api.py

from fastapi import APIRouter
from app.api.v1.endpoints import (
    image_generation, auth, character, chat, entity,
    feedback, conversation_intent, interaction, message, session,
    user, user_preference, models
)

api_router = APIRouter()

# AI and Chat related routes
api_router.include_router(character.router, prefix="/character", tags=["Character"])
api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])
api_router.include_router(models.router, prefix="/models", tags=["Models"])
api_router.include_router(image_generation.router, prefix="/image", tags=["Image Generation"])

# User related routes
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(user_preference.router, prefix="/user-preferences", tags=["User Preferences"])

# NLP related routes
api_router.include_router(entity.router, prefix="/entity", tags=["Entity"])
api_router.include_router(conversation_intent.router, prefix="/conversation-intent", tags=["Conversation Intent"])
api_router.include_router(interaction.router, prefix="/interaction", tags=["Interaction"])

# Session and Message routes
api_router.include_router(session.router, prefix="/session", tags=["Session"])
api_router.include_router(message.router, prefix="/messages", tags=["Messages"])

# Feedback route
api_router.include_router(feedback.router, prefix="/feedback", tags=["Feedback"])