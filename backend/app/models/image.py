# app/models/image.py

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class GeneratedImage(BaseModel):
    __tablename__ = "generated_images"

    user_id = Column(String(36), ForeignKey("users.user_id"))
    prompt = Column(String(255), index=True)
    prompt_id = Column(String(255), unique=True, index=True)
    image_url = Column(String(255))
    character_id = Column(ForeignKey("characters.id"))

    user = relationship("User", back_populates="generated_images")
    ai_personality = relationship("Character", back_populates="generated_images")