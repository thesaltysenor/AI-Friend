# app/services/nlp/user_input_analyzer.py

import logging
from typing import Union
from app.services.ai.lm_client import LMStudioClient
from app.models.messages import Message
from app.schemas.schemas import ChatInputMessage
from app.core.config import settings

class UserInputAnalyzer:
    def __init__(self):
        self.lm_client = LMStudioClient()

    async def categorize_input(self, user_input: str) -> str:
        try:
            prompt: str = f"Categorize the conversation intent of the following user input: '{user_input}'\nConversation Intent:"
            message: ChatInputMessage = ChatInputMessage(role="user", content=prompt, user_id="system")

            response: Union[Message, dict] = await self.lm_client.create_chat_completion(
                messages=[message],
                model=settings.CHOSEN_LM_MODEL,
                temperature=0.3,
                max_tokens=50
            )

            conversation_intent: str = "unknown"
            if isinstance(response, Message):
                conversation_intent = response.content.strip()
            elif isinstance(response, dict) and 'content' in response:
                conversation_intent = response['content'].strip()
            else:
                logging.warning(f"Unexpected response type: {type(response)}")

            logging.debug(f"Categorized conversation intent for input '{user_input}': {conversation_intent}")
            return conversation_intent
        except Exception as e:
            logging.exception(f"Error during input categorization: {e}")
            return "unknown"