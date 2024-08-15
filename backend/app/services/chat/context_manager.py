# app/services/chat/context_manager.py

import logging
from collections import deque
import time
from typing import List, Tuple, Dict, Optional
from app.models.messages import Message
from app.services.chat.context_triggers import ContextTriggers
from app.utils.text_cleaning import clean_ai_response
from app.utils.text_processing import post_process_response

class ChatContextManager:
    def __init__(self, max_length: int = 100, max_age: int = 900, decay_rate: float = 0.05):
        self.contexts: Dict[str, deque] = {}
        self.conversation_history: Dict[str, List[Tuple[Message, float]]] = {}
        self.max_length = max_length
        self.max_age = max_age  # max_age in seconds
        self.decay_rate = decay_rate  # Decay rate per minute
        self.context_triggers = ContextTriggers()

    def update_context(self, user_id: str, new_messages: List[Message]) -> None:
        """
        Update the context for a user with new messages.

        Args:
            user_id (str): The ID of the user whose context is being updated.
            new_messages (List[Message]): List of new messages to add to the context.
        """
        logging.debug(f"Received messages for update: {[{'role': m.role, 'content': m.content, 'timestamp': m.timestamp} for m in new_messages]}")

        context_queue = self._get_or_create_context_queue(user_id)
        current_time = time.time() 

        self._update_existing_messages(context_queue, current_time)
        new_messages = self._filter_new_messages(new_messages, current_time)
        self._add_new_messages(context_queue, new_messages)
        self._update_conversation_history(user_id, new_messages)
        self._trim_context_queue(context_queue)

        self._log_final_context_state(context_queue)

    def _get_or_create_context_queue(self, user_id: str) -> deque:
        """Get or create a context queue for a user."""
        return self.contexts.setdefault(user_id, deque())

    def _update_existing_messages(self, context_queue: deque, current_time: float) -> None:
        """Update relevance of existing messages and remove outdated ones."""
        context_queue_copy = list(context_queue)
        for msg in context_queue_copy:
            age_seconds = current_time - msg.timestamp
            if age_seconds >= self.max_age:
                context_queue.remove(msg)
                logging.debug(f"Removed message due to age: {msg.content}")
            elif not self._update_message_relevance(msg, age_seconds):
                context_queue.remove(msg)
                logging.debug(f"Removed message due to low relevance: {msg.content}")

    def _update_message_relevance(self, msg: Message, age_seconds: float) -> bool:
        """
        Update the relevance of a message based on its age.

        Args:
            msg (Message): The message to update.
            age_seconds (float): The age of the message in seconds.

        Returns:
            bool: True if the message is still relevant, False otherwise.
        """
        if msg.relevance is None:
            msg.relevance = 1.0
        msg.relevance -= self.decay_rate * (age_seconds / 60)
        if msg.relevance <= 0.1:
            logging.debug(f"Message relevance too low: {msg.content}")
            return False
        return True

    def _filter_new_messages(self, new_messages: List[Message], current_time: float) -> List[Message]:
        """Filter out messages that are too old."""
        return [msg for msg in new_messages if msg.timestamp is not None and current_time - msg.timestamp < self.max_age]

    def _add_new_messages(self, context_queue: deque, new_messages: List[Message]) -> None:
        """Add new messages to the context queue."""
        context_queue.extend(new_messages)
        logging.debug("New context queue state:")
        for msg in context_queue:
            logging.debug(f"Updated message: {msg.content}, timestamp: {msg.timestamp}")

    def _update_conversation_history(self, user_id: str, new_messages: List[Message]) -> None:
        """Update the conversation history for a user."""
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        timestamp = time.time()
        self.conversation_history[user_id].extend([(message, timestamp) for message in new_messages])

    def _trim_context_queue(self, context_queue: deque) -> None:
        """Trim the context queue to the maximum allowed length."""
        while len(context_queue) > self.max_length:
            removed_msg = context_queue.popleft()
            logging.debug(f"Removing message due to max length: {removed_msg.content}")

    def _log_final_context_state(self, context_queue: deque) -> None:
        """Log the final state of the context queue."""
        logging.debug("Final context state:")
        for msg in context_queue:
            logging.debug(f"Message: {msg.content}, Relevance: {msg.relevance}, Timestamp: {msg.timestamp}")
            
    def get_context(self, user_id: str, max_length: Optional[int] = None) -> List[Message]:
        """
        Get the current context for a user.

        Args:
            user_id (str): The ID of the user.
            max_length (Optional[int]): Maximum number of messages to return.

        Returns:
            List[Message]: List of context messages.
        """
        if user_id not in self.contexts:
            return []
        context = list(self.contexts[user_id])
        if max_length:
            context = context[-max_length:]
        return context

    def get_conversation_history(self, user_id: str, timestamp: Optional[float] = None) -> List[Tuple[Message, float]]:
        """
        Get the conversation history for a user.

        Args:
            user_id (str): The ID of the user.
            timestamp (Optional[float]): Optional timestamp to filter history from.

        Returns:
            List[Tuple[Message, float]]: List of tuples containing messages and their timestamps.
        """
        if user_id not in self.conversation_history:
            return []
        history = self.conversation_history[user_id]
        if timestamp:
            history = [(msg, ts) for msg, ts in history if ts >= timestamp]
        return history

    def clear_conversation_history(self, user_id: str) -> None:
        """
        Clear the conversation history for a user.

        Args:
            user_id (str): The ID of the user.
        """
        if user_id in self.conversation_history:
            self.conversation_history[user_id] = []

    def generate_response(self, user_id: str, message: Message, triggered_context: List[Message]) -> Message:
        """
        Generate a response based on the user's message and context.

        Args:
            user_id (str): The ID of the user.
            message (Message): The user's message.
            triggered_context (List[Message]): List of triggered context messages.

        Returns:
            Message: A generated response message.
        """
        # Check if there's a triggered context
        context_type = self.context_triggers.get_triggered_context(message.content)

        # Generate a response based on the user's message, context, and triggered context
        if context_type:
            response_content = f"Triggered context response ({context_type}) for user {user_id}: {message.content}"
        else:
            response_content = f"Generated response for user {user_id}: {message.content}"

        cleaned_response = clean_ai_response(response_content)
        processed_response = post_process_response(cleaned_response)
        return Message(role="assistant", content=processed_response)