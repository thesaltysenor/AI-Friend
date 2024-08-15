# app/services/nlp/nlp_service.py

import logging
from typing import List, Tuple, Dict, Any
import spacy
from nltk.sentiment import SentimentIntensityAnalyzer as NLTKAnalyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as VaderAnalyzer
from app.models.messages import Message

class NLPService:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.nltk_analyzer = NLTKAnalyzer()
        self.vader_analyzer = VaderAnalyzer()

    async def analyze_text(self, text: str) -> Dict[str, Any]:
        try:
            doc = self.nlp(text)
            tokens: List[Tuple[str, str]] = [(token.text, token.pos_) for token in doc]
            nltk_sentiment: dict = self.nltk_analyzer.polarity_scores(text)
            vader_sentiment: dict = self.vader_analyzer.polarity_scores(text)
            entities: List[Tuple[str, str]] = [(ent.text, ent.label_) for ent in doc.ents]
            
            # Determine overall sentiment
            compound_score = vader_sentiment['compound']
            if compound_score >= 0.05:
                overall_sentiment = "positive"
            elif compound_score <= -0.05:
                overall_sentiment = "negative"
            else:
                overall_sentiment = "neutral"

            return {
                "tokens": tokens,
                "nltk_sentiment": nltk_sentiment,
                "vader_sentiment": vader_sentiment,
                "overall_sentiment": overall_sentiment,
                "entities": entities,
                "primary_conversation_intent": self.extract_primary_intent(doc),
                "action_items": self.extract_action_items(doc)
            }
        except Exception as e:
            logging.exception(f"Error during text analysis: {str(e)}")
            raise

    def extract_primary_intent(self, doc: spacy.tokens.Doc) -> str:
        # Implement intent extraction logic
        # This is a placeholder implementation
        return "general_inquiry"

    def extract_action_items(self, doc: spacy.tokens.Doc) -> List[str]:
        # Implement action item extraction logic
        # This is a placeholder implementation
        return []

    async def analyze_user_input(self, messages: List[Message]) -> Dict[str, Any]:
        try:
            user_messages = " ".join([msg.content for msg in messages if msg.role == 'user'])
            return await self.analyze_text(user_messages)
        except Exception as e:
            logging.error(f"Error during user input analysis: {str(e)}")
            raise

    def extract_topics(self, text: str) -> List[str]:
        # Implement topic extraction logic
        # This is a placeholder implementation
        return ["machine learning", "natural language processing"]

    def recognize_entities(self, text: str) -> List[Tuple[str, str]]:
        try:
            doc = self.nlp(text)
            entities: List[Tuple[str, str]] = [(ent.text, ent.label_) for ent in doc.ents]
            return entities
        except Exception as e:
            logging.exception(f"Error during named entity recognition: {str(e)}")
            raise
        
    def adjust_response_based_on_sentiment(self, sentiment_results: Dict[str, Any], temperature: float) -> float:
        logging.info(f"Sentiment analysis results: {sentiment_results}")
        compound_score = sentiment_results['vader_sentiment']['compound']
        nltk_compound_score = sentiment_results['nltk_sentiment']['compound']
        
        combined_score = (compound_score + nltk_compound_score) / 2

        if combined_score <= -0.5:
            return 0.3  # Set to exactly 0.3 for highly negative sentiment
        elif combined_score < -0.3:
            return max(0.3, temperature - 0.2)
        elif combined_score > 0.5:
            return 0.9  # Set to exactly 0.9 for highly positive sentiment
        elif combined_score > 0.3:
            return min(0.9, temperature + 0.2)
        
        return temperature

    async def analyze_and_adjust_response(self, messages: List[Message], temperature: float) -> Tuple[Dict[str, Any], float]:
        try:
            text = " ".join([msg.content for msg in messages if msg.role == 'user'])
            sentiment_results = await self.analyze_text(text)
            adjusted_temperature = self.adjust_response_based_on_sentiment(sentiment_results, temperature)
            return sentiment_results, adjusted_temperature
        except Exception as e:
            logging.error(f"Error during sentiment analysis or adjustment: {e}")
            raise