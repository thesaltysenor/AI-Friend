# app/api/v1/endpoints/chat.py

from fastapi import APIRouter, Depends, HTTPException
from app.schemas import ChatInput, ChatInputMessage
from app.services.ai.lm_client import LMStudioClient
from app.services.chat.context_manager import ChatContextManager
from app.services.nlp.small_talk_module import SmallTalkModule
from app.services.ai.ai_personality import AIPersonality
from app.services.nlp.interaction_manager import InteractionManager
from app.services.db.ai_personality_manager import AIPersonalityManager
from app.services.ai.comfy_ui_service import ComfyUIService
from app.core.dependencies import get_comfy_ui_service
import logging
import time

router = APIRouter()
lm_client = LMStudioClient()
context_manager = ChatContextManager()
small_talk_module = SmallTalkModule()
interaction_manager = InteractionManager()

@router.post("/completions")
async def chat_endpoint(chat_input: ChatInput, comfy_ui: ComfyUIService = Depends(get_comfy_ui_service)):
    try:
        loaded_models = await lm_client.get_models()
        logging.debug(f"Loaded models: {loaded_models}")

        loaded_model_ids = [model["id"] for model in loaded_models["data"]]

        if chat_input.model not in loaded_model_ids:
            raise HTTPException(status_code=400, detail=f"Model '{chat_input.model}' is not loaded.")

        # Extract the last user message
        last_message: ChatInputMessage = chat_input.messages[-1]
        user_message = last_message.content
        user_id = last_message.user_id

        # Get context
        context = context_manager.get_context(user_id)
       
        ai_personality_manager = AIPersonalityManager()
    
        # If no AI personality is specified, use the default (adaptive) one
        ai_personality_id = chat_input.ai_personality_id or ai_personality_manager.get_or_create_default_ai_personality()
        
        # Create AIPersonality instance with the provided ai_personality_id
        ai_personality = AIPersonality(ai_personality_id)

        # Check if the message is requesting image generation
        if "generate image" in user_message.lower():
            image_prompt = extract_image_prompt(user_message)
            try:
                prompt_id = await comfy_ui.generate_image(image_prompt)
                generated_response = f"I'm generating an image for you based on: '{image_prompt}'. You can retrieve the image using this ID: {prompt_id}"
            except Exception as e:
                logging.error(f"Failed to generate image: {str(e)}")
                generated_response = "I'm sorry, but I couldn't generate the image at this time. Can I help you with anything else?"
        else:
            # Existing chat logic
            if small_talk_module.is_small_talk(user_message):
                generated_response = await small_talk_module.generate_small_talk_response(user_message, context)
            else:
                generated_response = await ai_personality.generate_response(user_message, context)

        logging.debug(f"Generated response: {generated_response}")

        # Update context
        context_manager.update_context(user_id, [generated_response])

        # Record interaction
        if ai_personality_id is None or not ai_personality_manager.get_ai_personality_by_id(ai_personality_id):
            ai_personality_id = ai_personality_manager.get_or_create_default_ai_personality()
    
        interaction_manager.create_interaction(user_id, ai_personality_id, "chat_completion")

        # Include adaptive traits in the response if applicable
        adaptive_traits = ai_personality.personality_traits if hasattr(ai_personality, 'personality_traits') else None

        return {
            "id": "chatcmpl-123",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": chat_input.model,
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
    
    except Exception as e:
        logging.error(f"API call failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"API call failed: {e}")
    
def extract_image_prompt(message: str) -> str:
    return message.lower().replace("generate image", "").strip()
    
def extract_image_prompt(message: str) -> str:
    return message.lower().replace("generate image", "").strip()
    
@router.get("/adaptive-traits/{character_id}")
async def get_adaptive_traits(character_id: int):
    try:
        ai_personality = AIPersonality(character_id)
        
        if ai_personality.personality_traits:
            return ai_personality.personality_traits
        else:
            # If no adaptive traits, return default traits
            return {
                "formality": 0,
                "enthusiasm": 0,
                "humor": 0,
                "empathy": 0,
            }
    except Exception as e:
        logging.error(f"Failed to get adaptive traits: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get adaptive traits")