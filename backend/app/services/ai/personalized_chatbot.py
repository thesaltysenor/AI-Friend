# app/services/ai/personalized_chatbot.py

import logging
import datetime
import random
from app.models.messages import Message
from app.schemas.schemas import ChatInputMessage
from app.services.ai.lm_client import LMStudioClient
from app.utils.text_cleaning import clean_ai_response
from app.utils.text_processing import post_process_response
from app.services.db.character_database import CharacterDatabase
from app.services.characters.character_details import get_character_details
from app.services.nlp.nlp_service import NLPService

class PersonalizedChatbot:
    def __init__(self, character_id=None, character_database=None):
        self.character_database = character_database
        self.nlp_service = NLPService()
        
        if character_id is None or character_id == 0:
            character_id = self.character_database.get_or_create_default_character()
        
        self.character = self.character_database.get_character_by_id(character_id)
        
        if self.character is None:
            logging.warning(f"No character found for id: {character_id}. Creating default adaptive personality.")
            character_id = self.character_database.get_or_create_default_character()
            self.character = self.character_database.get_character_by_id(character_id)
        
        self.character_details = get_character_details(self.character.character_type)
        self.lm_client = LMStudioClient()
        
        # Always initialize personality traits, defaulting to adaptive
        self.personality_traits = {
            "formality": 0,
            "enthusiasm": 0,
            "humor": 0,
            "empathy": 0,
        } if self.character.character_type == "adaptive" else None

    def get_system_prompt(self):
        base_prompt = f"""You are {self.character.name}. {self.character.description} 
        Your personality traits are: {self.character.personality_traits}.
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
            analysis = await self.nlp_service.analyze_text(message)
            
            # Adjust personality traits based on sentiment and conversation intent
            self.personality_traits["enthusiasm"] += analysis["vader_sentiment"]["compound"] * 0.1
            self.personality_traits["empathy"] += analysis["vader_sentiment"]["pos"] * 0.1

            if analysis["primary_conversation_intent"].lower() in ["joke", "humor"]:
                self.personality_traits["humor"] += 0.1
            elif analysis["primary_conversation_intent"].lower() in ["formal_request", "professional_inquiry"]:
                self.personality_traits["formality"] += 0.1

            # Cap values between -1 and 1
            for trait in self.personality_traits:
                self.personality_traits[trait] = max(-1, min(1, self.personality_traits[trait]))

    async def generate_response(self, user_input: str, context: list[Message]):
        if self.personality_traits:
            await self.analyze_message(user_input)
        logging.debug(f"Generating character response for input: {user_input}")
    
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
                temperature=0.7,
                max_tokens=150
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
                relevance=response.relevance
            )
            logging.debug(f"Cleaned response object: {cleaned_response}")
            logging.debug(f"Cleaned response content: {cleaned_response.content}")
            logging.debug(f"Cleaned response content type: {type(cleaned_response.content)}")

            return cleaned_response.content  # Return the content, not the Message object

        except Exception as e:
            logging.error(f"Error generating character response: {str(e)}")
            return "I apologize, but I am unable to generate a response at the moment."

    def prepare_input(self, user_input: str, context: list[Message]) -> str:
        return user_input

    def post_process_response(self, response: str) -> str:
        if self.character.character_type != "adaptive" and random.random() < 0.3:
            response += f" {random.choice(self.character_details['catchphrases'])}"
        return response