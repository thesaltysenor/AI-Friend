# app/models/image.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.services.db.base import Base
import datetime

class GeneratedImage(Base):
    __tablename__ = "generated_images"

    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(String, index=True)
    prompt_id = Column(String, unique=True, index=True)
    image_url = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    ai_personality_id = Column(Integer, ForeignKey("ai_personalities.id"))

    user = relationship("User", back_populates="generated_images")
    ai_personality = relationship("AIPersonality", back_populates="generated_images")