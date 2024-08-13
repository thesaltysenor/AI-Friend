# app/services/nlp/small_talk_module.py

import logging
import time
from app.schemas import ChatInputMessage
from app.models.messages import Message
from app.services.ai.lm_client import LMStudioClient
import datetime
from app.utils.text_cleaning import clean_ai_response
from app.utils.text_processing import post_process_response
# import CHOSEN_LM_MODEL from .env

class SmallTalkModule:
    def __init__(self):
        self.lm_client = LMStudioClient()

    async def generate_small_talk_response(self, user_input: str, context: list[Message]):
        logging.debug(f"Generating small talk response for user input: {user_input}")
        
        try:
            input_text = self.prepare_input(user_input, context)
            messages = [
                ChatInputMessage(role="system", content="You are a friendly conversational partner. Engage in natural dialogue without mentioning that you're an AI or a language model. Focus on the topic at hand and respond as a knowledgeable human would.", user_id="system"),
                ChatInputMessage(role="user", content=input_text, user_id="user")
            ]

            response = await self.lm_client.create_chat_completion(
                messages=messages,
                
                # import CHOSEN_LM_MODEL from .env
                model="mlabonne/AlphaMonarch-7B-GGUF/alphamonarch-7b.Q2_K.gguf",
                temperature=0.7,
                max_tokens=100
            )

            # Clean the response content
            cleaned_content = clean_ai_response(response.content)
            processed_content = post_process_response(cleaned_content)
            
            # Create a new Message object with the cleaned content
            cleaned_response = Message(
                role=response.role,
                content=processed_content,
                user_id=response.user_id,
                timestamp=response.timestamp,
                relevance=response.relevance
            )

            return cleaned_response

        except Exception as e:
            logging.error(f"Error generating small talk response: {str(e)}")
            return Message(
                role="assistant",
                content="I apologize, but I am unable to generate a response at the moment.",
                user_id="assistant",
                timestamp=datetime.datetime.now().timestamp(),
                relevance=1.0
            )

    def prepare_input(self, user_input: str, context: list[Message]) -> str:
        context_text = " ".join([f"{message.role}: {message.content}" for message in context])
        return f"Generate a friendly small talk response to the following conversation:\n\n{context_text}\nUser: {user_input}\nAssistant:"

    def is_small_talk(self, user_input: str) -> bool:
        logging.debug(f"Checking if user input is small talk: {user_input}")

        small_talk_patterns = [
            "hello", "hi", "hey", "how are you", "how's it going", "what's up",
            "how's your day", "nice to meet you", "good morning", "good afternoon",
            "good evening", "goodbye", "bye", "see you later"
        ]

        user_input = user_input.lower()
        for pattern in small_talk_patterns:
            if pattern in user_input:
                logging.debug(f"User input '{user_input}' matches small talk pattern: {pattern}")
                logging.debug(f"User input is small talk: {user_input}")
                return True

        logging.debug(f"User input is not small talk: {user_input}")
        return False