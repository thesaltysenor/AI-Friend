# app/models/image.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.services.db.database import Base
import datetime

class GeneratedImage(Base):
    __tablename__ = "generated_images"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(36), ForeignKey("users.user_id"))
    prompt = Column(String(255), index=True)
    prompt_id = Column(String(255), unique=True, index=True)
    image_url = Column(String(255))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    ai_personality_id = Column(Integer, ForeignKey("ai_personalities.id"))

    user = relationship("User", back_populates="generated_images")
    ai_personality = relationship("AIPersonality", back_populates="generated_images")