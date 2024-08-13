# app/services/nlp/intent_recognizer.py

import logging
from app.services.ai.lm_client import LMStudioClient
from app.models.messages import Message
from app.schemas.schemas import ChatInputMessage
# import CHOSEN_LM_MODEL from .env

class IntentRecognizer:
    def __init__(self):
        self.lm_client = LMStudioClient()

    async def recognize_intent(self, user_input):
        try:
            # Prepare the prompt for intent recognition
            prompt = f"Recognize the intent of the following user input: '{user_input}'\nIntent:"
        
            # Create a proper ChatInputMessage object
            message = ChatInputMessage(role="user", content=prompt, user_id="system")

            # Use the LM Studio API to generate a response
            response = await self.lm_client.create_chat_completion(
                messages=[message],
                
                # import CHOSEN_LM_MODEL from .env
                model="mlabonne/AlphaMonarch-7B-GGUF/alphamonarch-7b.Q2_K.gguf",
                temperature=0.3,
                max_tokens=50
            )

            # Extract the intent from the response
            if isinstance(response, Message):
                intent = response.content.strip()
            elif isinstance(response, dict) and 'content' in response:
                intent = response['content'].strip()
            else:
                logging.warning(f"Unexpected response type: {type(response)}")
                intent = "unknown"

            logging.debug(f"Recognized intent for input '{user_input}': {intent}")
            return intent
        except Exception as e:
            logging.error(f"Error during intent recognition: {e}", exc_info=True)
            return "unknown"