# app/models/ai_personality.py
from sqlalchemy import Column, Integer, String, Boolean, Text
from app.services.db.base import Base
from sqlalchemy.orm import relationship

class AIPersonality(Base):
    __tablename__ = "ai_personality"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    description = Column(Text)
    personality_traits = Column(Text)
    available = Column(Boolean, default=True)
    character_type = Column(String(50), default="default")

    
    # Relationships
    interactions = relationship("Interaction", back_populates="ai_personality")
    generated_images = relationship("GeneratedImage", back_populates="ai_personality")


    