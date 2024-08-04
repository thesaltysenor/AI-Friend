from fastapi import APIRouter
from app.api.v1.endpoints import image_generation, auth, ai_personality, chat, entity, feedback, intent, interaction, message, session, user, user_preference, models


api_router = APIRouter()

api_router.include_router(ai_personality.router, prefix="/ai-personality", tags=["AI Personality"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])
api_router.include_router(entity.router, prefix="/entity", tags=["Entity"])
api_router.include_router(feedback.router, prefix="/feedback", tags=["Feedback"])
api_router.include_router(intent.router, prefix="/intent", tags=["Intent"])
api_router.include_router(interaction.router, prefix="/interaction", tags=["Interaction"])
api_router.include_router(message.router, prefix="/messages", tags=["Messages"])
api_router.include_router(session.router, prefix="/session", tags=["Session"])
api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(user_preference.router, prefix="/user-preferences", tags=["User Preferences"])
api_router.include_router(models.router, prefix="/models", tags=["Models"])
api_router.include_router(image_generation.router, prefix="/image", tags=["image"])

