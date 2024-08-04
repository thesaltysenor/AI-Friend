# app/services/context_triggers.py

import re

class ContextTriggers:
    def __init__(self):
        self.context_triggers = {
            "greeting": re.compile(r"\b(hello|hi|hey)\b", re.IGNORECASE),
            "farewell": re.compile(r"\b(bye|goodbye|see you)\b", re.IGNORECASE),
            "thanks": re.compile(r"\b(thank you|thanks|appreciate)\b", re.IGNORECASE),
            "help": re.compile(r"\b(help|assistance|support)\b", re.IGNORECASE)
        }

    def add_context_trigger(self, context, trigger_pattern):
        self.context_triggers[context] = re.compile(trigger_pattern, re.IGNORECASE)

    def get_triggered_context(self, user_input):
        for context, pattern in self.context_triggers.items():
            if pattern.search(user_input):
                return context
        return None
    
    def remove_context_trigger(self, context):
        if context in self.context_triggers:
            del self.context_triggers[context]