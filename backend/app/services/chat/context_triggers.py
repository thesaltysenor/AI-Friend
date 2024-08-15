# app/services/chat/context_triggers.py

import re
from typing import Dict, Optional, Pattern

class ContextTriggers:
    def __init__(self):
        self.context_triggers: Dict[str, Pattern] = {
            "greeting": re.compile(r"\b(hello|hi|hey)\b", re.IGNORECASE),
            "farewell": re.compile(r"\b(bye|goodbye|see you)\b", re.IGNORECASE),
            "thanks": re.compile(r"\b(thank you|thanks|appreciate)\b", re.IGNORECASE),
            "help": re.compile(r"\b(help|assistance|support)\b", re.IGNORECASE)
        }

    def add_context_trigger(self, context: str, trigger_pattern: str) -> None:
        """
        Add a new context trigger.

        Args:
            context (str): The name of the context.
            trigger_pattern (str): The regex pattern to trigger this context.
        """
        self.context_triggers[context] = re.compile(trigger_pattern, re.IGNORECASE)

    def get_triggered_context(self, user_input: str) -> Optional[str]:
        """
        Get the triggered context based on user input.

        Args:
            user_input (str): The user's input message.

        Returns:
            Optional[str]: The name of the triggered context, or None if no context was triggered.
        """
        for context, pattern in self.context_triggers.items():
            if pattern.search(user_input):
                return context
        return None
    
    def remove_context_trigger(self, context: str) -> None:
        """
        Remove a context trigger.

        Args:
            context (str): The name of the context to remove.
        """
        if context in self.context_triggers:
            del self.context_triggers[context]