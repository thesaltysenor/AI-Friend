# app/models/entity.py
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class Entity(BaseModel):
    __tablename__ = "entities"

    entity_name = Column(String(100), index=True)
    conversation_intent_id = Column(ForeignKey('conversation_intents.id'))

    conversation_intent = relationship("ConversationIntent", back_populates="entities")