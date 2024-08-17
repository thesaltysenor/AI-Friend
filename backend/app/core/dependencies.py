# app/core/dependencies.py

import asyncio
import os
from typing import Optional, Generator
from sqlalchemy.orm import Session
from fastapi import Depends
from app.services.db.database_setup import SessionLocal

from app.services.ai.comfy_ui_service import ComfyUIService
from app.services.ai.lm_client import LMStudioClient
from app.services.chat.context_manager import ChatContextManager
from app.services.nlp.casual_conversation_handler import CasualConversation
from app.services.db.interaction_manager import InteractionManager
from app.services.db.character_database import CharacterDatabase
from app.services.db.user_manager import UserManager
from app.services.db.user_preference_manager import UserPreferenceManager
from app.services.db.session_manager import SessionManager
from app.services.db.message_manager import MessageManager
from app.services.db.conversation_intent_manager import ConversationIntentManager
from app.services.nlp.nlp_service import NLPService
from app.services.chat.chat_response_handler import ChatResponseHandler

# ComfyUIService instance
_comfy_ui_service = None

def get_comfy_ui_service() -> ComfyUIService:
    global _comfy_ui_service
    if _comfy_ui_service is None:
        _comfy_ui_service = ComfyUIService()
    return _comfy_ui_service

async def get_prediction(input_text: str) -> Optional[str]:
    node_script_path = os.path.join(os.path.dirname(__file__), 'lm_client.ts')
    cmd = ['node', node_script_path, input_text]

    try:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            return stdout.decode()
        else:
            error_msg = stderr.decode()
            print(f"Error running lm_client.ts: {error_msg}")
            return None
    except Exception as e:
        print(f"Exception occurred while running lm_client.ts: {str(e)}")
        return None

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_lm_client():
    return LMStudioClient()

def get_context_manager():
    return ChatContextManager()

def get_casual_conversation_handler():
    return CasualConversation()

def get_character_database(db: Session = Depends(get_db)) -> CharacterDatabase:
    return CharacterDatabase(db)

def get_user_manager(db: Session = Depends(get_db)):
    return UserManager(db)

def get_user_preference_manager(db: Session = Depends(get_db)):
    return UserPreferenceManager(db)

def get_session_manager(db: Session = Depends(get_db)):
    return SessionManager(db)

def get_message_manager(db: Session = Depends(get_db)):
    return MessageManager(db)

def get_conversation_intent_manager(db: Session = Depends(get_db)):
    return ConversationIntentManager(db)

def get_nlp_service():
    return NLPService()

def get_interaction_manager(db: Session = Depends(get_db)):
    return InteractionManager(db)

def get_chat_response_handler():
    return ChatResponseHandler()