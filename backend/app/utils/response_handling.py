# app/response_handling.py

import logging

from fastapi import HTTPException
from app.services.nlp.nlp_service import SentimentAnalysis

def adjust_response_based_on_sentiment(sentiment_results, chat_input):
    logging.info(f"Sentiment analysis results: {sentiment_results}")
    compound_score = sentiment_results['vader_sentiment']['compound']
    nltk_compound_score = sentiment_results['nltk_sentiment']['compound']
    
    # Combining the results from both sentiment analysis
    combined_score = (compound_score + nltk_compound_score) / 2

    if combined_score <= -0.5:
        chat_input.temperature = 0.3  # Set to exactly 0.3 for highly negative sentiment
    elif combined_score < -0.3:
        chat_input.temperature = max(0.3, chat_input.temperature - 0.2)
    elif combined_score > 0.5:
        chat_input.temperature = 0.9  # Set to exactly 0.9 for highly positive sentiment
    elif combined_score > 0.3:
        chat_input.temperature = min(0.9, chat_input.temperature + 0.2)

    return chat_input

def analyze_and_adjust_response(messages, chat_input):
    sentiment_analyzer = SentimentAnalysis()
    try:
        text = " ".join([msg.content for msg in messages if msg.role == 'user'])
        sentiment_results = sentiment_analyzer.analyze_text(text)
        chat_input = adjust_response_based_on_sentiment(sentiment_results, chat_input)
    except Exception as e:
        logging.error(f"Error during sentiment analysis or adjustment: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze and adjust response based on sentiment")
    return chat_input

def handle_conversation_intent(recognized_conversation_intent, user_message, context):
    if recognized_conversation_intent == "greeting":
        return "Hello! How can I assist you today?"
    elif recognized_conversation_intent == "help":
        return "Sure, I'm here to help. What do you need assistance with?"
    else:
        return None

def handle_context(triggered_context, user_message, context):
    if triggered_context == "farewell":
        return "Goodbye! Have a great day!"
    elif triggered_context == "thanks":
        return "You're welcome! It's my pleasure to help."
    else:
        return None