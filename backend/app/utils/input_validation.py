# app/utils/input_validation.py

import re

def sanitize_prompt(prompt: str) -> str:
    # Remove any characters that aren't alphanumeric, spaces, or common punctuation
    sanitized = re.sub(r'[^a-zA-Z0-9\s.,!?-]', '', prompt)
    # Limit the length of the prompt
    return sanitized[:1000]  # Adjust the max length as needed