# app/api/v1/endpoints/chat.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import ChatInput, ChatInputMessage, ImageGenerationRequest, ImageGenerationResponse
from app.services.ai.lm_client import LMStudioClient
from app.services.chat.context_manager import ChatContextManager
from app.services.nlp.casual_conversation_handler import CasualConversation
from app.services.ai.personalized_chatbot import PersonalizedChatbot
from app.services.db.interaction_manager import InteractionManager
from app.services.db.character_database import CharacterDatabase
from app.services.ai.comfy_ui_service import ComfyUIService
from app.core.dependencies import (
    get_db,
    get_comfy_ui_service,
    get_lm_client,
    get_context_manager,
    get_casual_conversation_handler,
    get_interaction_manager,
    get_character_database
)
import logging
from typing import Dict, Any, List, Optional
import time

router = APIRouter()

# Constants
GENERATE_IMAGE = "generate image"

@router.post("/completions", response_model=Dict[str, Any])
async def chat_endpoint(
    chat_input: ChatInput,
    db: Session = Depends(get_db),
    comfy_ui: ComfyUIService = Depends(get_comfy_ui_service),
    lm_client: LMStudioClient = Depends(get_lm_client),
    context_manager: ChatContextManager = Depends(get_context_manager),
    casual_conversation_handler: CasualConversation = Depends(get_casual_conversation_handler),
    interaction_manager: InteractionManager = Depends(get_interaction_manager),
    character_database: CharacterDatabase = Depends(get_character_database)
):
    try:
        # Validate model
        loaded_models = await lm_client.get_models()
        if chat_input.model not in [model["id"] for model in loaded_models["data"]]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Model '{chat_input.model}' is not loaded."
            )

        # Extract user message and context
        last_message: ChatInputMessage = chat_input.messages[-1]
        user_message = last_message.content
        user_id = last_message.user_id
        context = context_manager.get_context(user_id)

        # Get or create character
        character_id = chat_input.ai_personality_id or character_database.get_or_create_default_character()
        personalized_chatbot = PersonalizedChatbot(character_id)

        # Generate response
        if GENERATE_IMAGE in user_message.lower():
            return await generate_image(user_message, character_id, comfy_ui)
        else:
            generated_response = await generate_chat_response(
                user_message,
                context,
                casual_conversation_handler,
                personalized_chatbot
            )

        # Update context and record interaction
        context_manager.update_context(user_id, [generated_response])
        interaction_manager.create_interaction(user_id, character_id, "chat_completion")

        # Get adaptive traits
        character = character_database.get_character_by_id(character_id)
        adaptive_traits = character.personality_traits if character else None

        return format_chat_response(chat_input.model, generated_response, adaptive_traits)

    except Exception as e:
        logging.error(f"API call failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

async def generate_image(user_message: str, character_id: int, comfy_ui: ComfyUIService) -> ImageGenerationResponse:
    image_request = ImageGenerationRequest(prompt=extract_image_prompt(user_message), ai_personality_id=character_id)
    try:
        prompt_id = await comfy_ui.generate_image(image_request.prompt)
        return ImageGenerationResponse(
            prompt_id=prompt_id,
            message=f"I'm generating an image for you based on: '{image_request.prompt}'. You can retrieve the image using this ID: {prompt_id}"
        )
    except Exception as e:
        logging.error(f"Failed to generate image: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate image"
        )

async def generate_chat_response(
    user_message: str,
    context: List[str],
    casual_conversation_handler: CasualConversation,
    personalized_chatbot: PersonalizedChatbot
) -> str:
    if casual_conversation_handler.casual_conversation(user_message):
        return await casual_conversation_handler.generate_casual_conversation_response(user_message, context)
    else:
        return await personalized_chatbot.generate_response(user_message, context)

def extract_image_prompt(message: str) -> str:
    return message.lower().replace(GENERATE_IMAGE, "").strip()

def format_chat_response(model: str, generated_response: str, adaptive_traits: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "id": f"chatcmpl-{int(time.time())}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": generated_response
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0
        },
        "adaptive_traits": adaptive_traits
    }

@router.get("/adaptive-traits/{character_id}")
async def get_adaptive_traits(
    character_id: int,
    character_database: CharacterDatabase = Depends(get_character_database)
):
    try:
        character = character_database.get_character_by_id(character_id)
        
        if character and character.personality_traits:
            return character.personality_traits
        else:
            return {
                "formality": 0,
                "enthusiasm": 0,
                "humor": 0,
                "empathy": 0,
            }
    except Exception as e:
        logging.error(f"Failed to get adaptive traits: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get adaptive traits")