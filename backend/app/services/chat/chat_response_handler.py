# app/services/chat/response_handler.py

from typing import Optional, Dict, Any

class ChatResponseHandler:
    @staticmethod
    def handle_conversation_intent(recognized_conversation_intent: str, user_message: str, context: Dict[str, Any]) -> Optional[str]:
        if recognized_conversation_intent == "greeting":
            return "Hello! How can I assist you today?"
        elif recognized_conversation_intent == "help":
            return "Sure, I'm here to help. What do you need assistance with?"
        else:
            return None

    @staticmethod
    def handle_context(triggered_context: str, user_message: str, context: Dict[str, Any]) -> Optional[str]:
        if triggered_context == "farewell":
            return "Goodbye! Have a great day!"
        elif triggered_context == "thanks":
            return "You're welcome! It's my pleasure to help."
        else:
            return None