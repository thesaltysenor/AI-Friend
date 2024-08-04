# app/models/interaction.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.services.db.base import Base
from datetime import datetime

class Interaction(Base):
    __tablename__ = "interaction"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(36), ForeignKey('users.user_id'))
    ai_personality_id = Column(Integer, ForeignKey('ai_personality.id'))
    interaction_type = Column(String(100))
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="interactions")
    ai_personality = relationship("AIPersonality", back_populates="interactions")