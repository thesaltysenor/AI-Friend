# app/services/nlp/small_talk_module.py

import logging
import datetime
from typing import List
from app.schemas import ChatInputMessage
from app.models.messages import Message
from app.services.ai.lm_client import LMStudioClient
from app.utils.text_cleaning import clean_ai_response
from app.utils.text_processing import post_process_response

class CasualConversation:
    def __init__(self):
        self.lm_client = LMStudioClient()

    async def generate_casual_conversation_response(self, user_input: str, context: List[Message]) -> Message:
        """
        Generate a casual conversation response based on user input and context.

        Args:
            user_input (str): The user's input message.
            context (List[Message]): The conversation context.

        Returns:
            Message: The generated response message.
        """
        logging.debug(f"Generating small talk response for user input: {user_input}")
        
        try:
            input_text = self.prepare_input(user_input, context)
            messages = [
                ChatInputMessage(role="system", content="You are a friendly conversational partner. Engage in natural dialogue without mentioning that you're an AI or a language model. Focus on the topic at hand and respond as a knowledgeable human would.", user_id="system"),
                ChatInputMessage(role="user", content=input_text, user_id="user")
            ]

            response = await self.lm_client.create_chat_completion(
                messages=messages,
                # use .env to import lm model for cleaner code
                model="mlabonne/AlphaMonarch-7B-GGUF/alphamonarch-7b.Q2_K.gguf",
                temperature=0.7,
                max_tokens=100
            )

            cleaned_content = clean_ai_response(response.content)
            processed_content = post_process_response(cleaned_content)
            
            return Message(
                role=response.role,
                content=processed_content,
                user_id=response.user_id,
                timestamp=response.timestamp,
                relevance=response.relevance
            )

        except Exception as e:
            logging.error(f"Error generating casual response: {str(e)}")
            return Message(
                role="assistant",
                content="I apologize, but I am unable to generate a response at the moment.",
                user_id="assistant",
                timestamp=datetime.datetime.now().timestamp(),
                relevance=1.0
            )

    def prepare_input(self, user_input: str, context: List[Message]) -> str:
        """
        Prepare the input for the language model.

        Args:
            user_input (str): The user's input message.
            context (List[Message]): The conversation context.

        Returns:
            str: The prepared input string.
        """
        context_text = " ".join([f"{message.role}: {message.content}" for message in context])
        return f"Generate a friendly casual response to the following conversation:\n\n{context_text}\nUser: {user_input}\nAssistant:"

    def casual_conversation(self, user_input: str) -> bool:
        """
        Check if the user input is considered casual conversation.

        Args:
            user_input (str): The user's input message.

        Returns:
            bool: True if the input is considered casual conversation, False otherwise.
        """
        logging.debug(f"Checking if user input is casual conversation: {user_input}")

        casual_conversation_patterns = [
            "hello", "hi", "hey", "how are you", "how's it going", "what's up",
            "how's your day", "nice to meet you", "good morning", "good afternoon",
            "good evening", "goodbye", "bye", "see you later"
        ]

        user_input = user_input.lower()
        for pattern in casual_conversation_patterns:
            if pattern in user_input:
                logging.debug(f"User input '{user_input}' matches casual conversation pattern: {pattern}")
                return True

        logging.debug(f"User input is not casual conversation: {user_input}")
        return False