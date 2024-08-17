# app/models/character.py
from sqlalchemy import Column, String, Boolean, Text
from sqlalchemy.orm import relationship
from .base import BaseModel

class Character(BaseModel):
    __tablename__ = "characters"

    name = Column(String(255), nullable=False)
    description = Column(Text)
    personality_traits = Column(Text)
    available = Column(Boolean, default=True)
    character_type = Column(String(50), default="default")

    interactions = relationship("Interaction", back_populates="character")
    generated_images = relationship("GeneratedImage", back_populates="character")