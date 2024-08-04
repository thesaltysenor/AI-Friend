# app/services/context_manager.py

import logging
from collections import deque
import time
from typing import List, Tuple
from app.models.messages import Message
from app.services.chat.context_triggers import ContextTriggers
from app.utils.text_cleaning import clean_ai_response
from app.utils.text_processing import post_process_response
class ChatContextManager:
    def __init__(self, max_length=100, max_age=900, decay_rate=0.05):
        self.contexts = {}
        self.conversation_history = {}
        self.max_length = max_length
        self.max_age = max_age  # max_age in seconds
        self.decay_rate = decay_rate  # Decay rate per minute
        self.context_triggers = ContextTriggers()

    def update_context(self, user_id: str, new_messages: List[Message]):    
        logging.debug(f"Received messages for update: {[{'role': m.role, 'content': m.content, 'timestamp': m.timestamp} for m in new_messages]}")

        if user_id not in self.contexts:
            self.contexts[user_id] = deque()
        context_queue = self.contexts[user_id]
        current_time = time.time() 

        # Decrement relevance of existing messages and remove them if they're too old or irrelevant
        for msg in list(context_queue):  # Use a list to avoid modifying the deque during iteration
            logging.debug(f"Processing existing message with timestamp: {msg.timestamp}")

            age_seconds = current_time - msg.timestamp  # Calculate age in seconds
            if age_seconds >= self.max_age:
                context_queue.remove(msg)
                logging.debug(f"Removed message due to age: {msg.content}")
            else:
                if msg.relevance is None:
                    msg.relevance = 1.0  # Set a default relevance if it's None
                msg.relevance -= self.decay_rate * (age_seconds / 60)
                if msg.relevance <= 0.1:
                    context_queue.remove(msg)
                    logging.debug(f"Removed message due to low relevance: {msg.content}")
                    
        # Remove messages from the new_messages list that are too old
        new_messages = [msg for msg in new_messages if msg.timestamp is not None and current_time - msg.timestamp < self.max_age]

        # Add new messages
        context_queue.extend(new_messages)
        logging.debug("New context queue state:")
        for msg in context_queue:
            logging.debug(f"Updated message: {msg.content}, timestamp: {msg.timestamp}")

        # Append new messages to the conversation history with timestamps and user ID
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        timestamp = time.time()
        self.conversation_history[user_id].extend([(message, timestamp) for message in new_messages])

        # Ensure the context does not exceed the maximum length
        while len(context_queue) > self.max_length:
            removed_msg = context_queue.popleft()
            logging.debug(f"Removing message due to max length: {removed_msg.content}")

        logging.debug("Final context state:")
        for msg in context_queue:
            logging.debug(f"Message: {msg.content}, Relevance: {msg.relevance}, Timestamp: {msg.timestamp}")

    def get_context(self, user_id: str, max_length: int = None) -> List[Message]:
        if user_id not in self.contexts:
            return []
        context = list(self.contexts[user_id])
        if max_length:
            context = context[-max_length:]
        return context

    def get_conversation_history(self, user_id: str, timestamp: float = None) -> List[Tuple[Message, float]]:
        if user_id not in self.conversation_history:
            return []
        history = self.conversation_history[user_id]
        if timestamp:
            history = [(msg, ts) for msg, ts in history if ts >= timestamp]
        return history

    def clear_conversation_history(self, user_id: str):
        if user_id in self.conversation_history:
            self.conversation_history[user_id] = []

    def generate_response(self, user_id: str, message: Message, triggered_context: List[Message]) -> Message:
        # Get the triggered context
        triggered_context = self.context_triggers.get_triggered_context(message.content)

        # Generate a response based on the user's message, context, and triggered context
        if triggered_context:
            response_content = f"Triggered context response for user {user_id}: {message.content}"
        else:
            response_content = f"Generated response for user {user_id}: {message.content}"

        cleaned_response = clean_ai_response(response_content)
        processed_response = post_process_response(cleaned_response)
        return Message(role="assistant", content=processed_response)
    