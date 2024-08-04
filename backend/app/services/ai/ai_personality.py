# app/services/ai/ai_personality.py

import logging
import datetime
import random
from app.models.messages import Message
from app.schemas import ChatInputMessage
from app.services.ai.lm_client import LMStudioClient
from app.utils.text_cleaning import clean_ai_response
from app.utils.text_processing import post_process_response
from app.services.db.ai_personality_manager import AIPersonalityManager
from app.services.characters.character_details import get_character_details
from app.services.nlp.nlp_service import SentimentAnalysis
from app.services.nlp.intent_recognizer import IntentRecognizer

class AIPersonality:
    def __init__(self, ai_personality_id=None):
        self.ai_personality_manager = AIPersonalityManager()
        self.sentiment_analyzer = SentimentAnalysis()
        self.intent_recognizer = IntentRecognizer()
        
        if ai_personality_id is None or ai_personality_id == 0:
            ai_personality_id = self.ai_personality_manager.get_or_create_default_ai_personality()
        
        self.ai_personality = self.ai_personality_manager.get_ai_personality_by_id(ai_personality_id)
        
        if self.ai_personality is None:
            logging.warning(f"No AI personality found for id: {ai_personality_id}. Creating default adaptive personality.")
            ai_personality_id = self.ai_personality_manager.get_or_create_default_ai_personality()
            self.ai_personality = self.ai_personality_manager.get_ai_personality_by_id(ai_personality_id)
        
        self.character_details = get_character_details(self.ai_personality.character_type)
        self.lm_client = LMStudioClient()
        
        # Always initialize personality traits, defaulting to adaptive
        self.personality_traits = {
            "formality": 0,
            "enthusiasm": 0,
            "humor": 0,
            "empathy": 0,
        } if self.ai_personality.character_type == "adaptive" else None

    def get_default_personality(self):
        # This method is no longer needed, but kept for backwards compatibility
        return self.ai_personality_manager.get_or_create_default_ai_personality()

    def get_system_prompt(self):
        base_prompt = f"""You are {self.ai_personality.name}. {self.ai_personality.description} 
        Your personality traits are: {self.ai_personality.personality_traits}.
        Backstory: {self.character_details['backstory']}
        Speak in a {self.character_details['speech_style']} manner.
        You have expertise in: {', '.join(self.character_details['knowledge_areas'])}."""

        if self.personality_traits:
            adaptive_prompt = self.generate_adaptive_prompt()
            base_prompt += f"\n{adaptive_prompt}"

        return base_prompt

    def generate_adaptive_prompt(self):
        prompts = []
        if self.personality_traits["formality"] > 0.5:
            prompts.append("Speak formally and professionally.")
        elif self.personality_traits["formality"] < -0.5:
            prompts.append("Speak casually and informally.")
        if self.personality_traits["enthusiasm"] > 0.5:
            prompts.append("Be very enthusiastic and energetic in your responses.")
        elif self.personality_traits["enthusiasm"] < -0.5:
            prompts.append("Remain calm and composed in your responses.")
        if self.personality_traits["humor"] > 0.5:
            prompts.append("Incorporate humor and light-heartedness in your responses.")
        elif self.personality_traits["humor"] < -0.5:
            prompts.append("Maintain a serious and straightforward tone.")
        if self.personality_traits["empathy"] > 0.5:
            prompts.append("Show strong empathy and emotional understanding.")
        elif self.personality_traits["empathy"] < -0.5:
            prompts.append("Focus on facts and logic rather than emotions.")

        return " ".join(prompts)
    

    async def analyze_message(self, message: str):
        if self.personality_traits:
            sentiment = self.sentiment_analyzer.analyze_text(message)
            intent = await self.intent_recognizer.recognize_intent(message)

            # Adjust personality traits based on sentiment and intent
            self.personality_traits["enthusiasm"] += sentiment["vader_sentiment"]["compound"] * 0.1
            self.personality_traits["empathy"] += sentiment["vader_sentiment"]["pos"] * 0.1

            if intent.lower() in ["joke", "humor"]:
                self.personality_traits["humor"] += 0.1
            elif intent.lower() in ["formal_request", "professional_inquiry"]:
                self.personality_traits["formality"] += 0.1

            # Cap values between -1 and 1
            for trait in self.personality_traits:
                self.personality_traits[trait] = max(-1, min(1, self.personality_traits[trait]))

    async def generate_response(self, user_input: str, context: list[Message]):
        if self.personality_traits:
            await self.analyze_message(user_input)
        logging.debug(f"Generating AI personality response for input: {user_input}")
        
        try:
            input_text = self.prepare_input(user_input, context)
            messages = [
                ChatInputMessage(role="system", content=self.get_system_prompt(), user_id="system"),
                *[ChatInputMessage(role=msg.role, content=msg.content, user_id=msg.user_id) for msg in context],
                ChatInputMessage(role="user", content=input_text, user_id="user")
            ]

            response = await self.lm_client.create_chat_completion(
                messages=messages,
                model="mlabonne/AlphaMonarch-7B-GGUF/alphamonarch-7b.Q2_K.gguf",
                temperature=0.7, # lower for more focused responses
                max_tokens=150  # adjusted for concise responses
            )

            # Clean the response content
            cleaned_content = clean_ai_response(response.content)
            processed_content = post_process_response(cleaned_content)
            processed_content = self.post_process_response(processed_content)
            
            # Create a new Message object with the cleaned content
            cleaned_response = Message(
                role=response.role,
                content=processed_content,
                user_id=response.user_id,
                timestamp=response.timestamp,
                relevance=response.relevance,
                adaptive_traits=self.personality_traits if self.personality_traits else None
            )

            return cleaned_response

        except Exception as e:
            logging.error(f"Error generating AI personality response: {str(e)}")
            return Message(
                role="assistant",
                content="I apologize, but I am unable to generate a response at the moment.",
                user_id="assistant",
                timestamp=datetime.datetime.now().timestamp(),
                relevance=1.0,
                adaptive_traits=self.personality_traits if self.personality_traits else None
            )

    def prepare_input(self, user_input: str, context: list[Message]) -> str:
        return user_input

    def post_process_response(self, response: str) -> str:
        if self.ai_personality.character_type != "adaptive" and random.random() < 0.3:
            response += f" {random.choice(self.character_details['catchphrases'])}"
        return response