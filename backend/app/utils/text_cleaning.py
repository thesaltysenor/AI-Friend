import re

def clean_ai_response(response: str) -> str:
    # Remove the "(Answering the user with" part and anything after it
    response = re.split(r'\(Answering the user with', response)[0]
    
    # Remove any (/Spark...) or similar parenthetical comments
    response = re.sub(r'\([^)]*\)', '', response)
    
    # Remove non-ASCII characters (this will remove emojis and other special characters)
    response = re.sub(r'[^\x00-\x7F]+', '', response)
    
    # Remove single non-alphabet characters between words
    response = re.sub(r'\s[^a-zA-Z\s]\s', ' ', response)
    
    # Remove nonsensical words (you can add more as needed)
    nonsense_words = ['delep']
    for word in nonsense_words:
        response = re.sub(r'\b' + word + r'\b', '', response, flags=re.IGNORECASE)
    
    # Remove extra whitespace
    response = ' '.join(response.split())
    
    return response.strip()