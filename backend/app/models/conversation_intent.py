# app/models/conversation_intent.py
from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from .base import BaseModel

class ConversationIntent(BaseModel):
    __tablename__ = "conversation_intents"

    conversation_intent_name = Column(String(100), index=True)
    description = Column(Text)

    entities = relationship("Entity", back_populates="conversation_intent")