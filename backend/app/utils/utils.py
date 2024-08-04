# app/utils.py

import logging
from app.services.ai.lm_client import LMStudioClient

def analyze_user_sentiment(messages):
    try:
        lm_client = LMStudioClient()
        user_messages = " ".join([msg.content for msg in messages if msg.role == 'user'])
        sentiment_results = lm_client.get_message_sentiment(user_messages)  # Verify this method exists
        logging.info(f"Sentiment analysis results: {sentiment_results}")
        return sentiment_results
    except Exception as e:
        logging.error(f"Error during sentiment analysis: {str(e)}")
        raise