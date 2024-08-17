# app/models/interaction.py
from datetime import datetime
from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel


class Interaction(BaseModel):
    __tablename__ = "interactions"

    user_id = Column(String(36), ForeignKey('users.user_id'))
    character_id = Column(ForeignKey('characters.id'))
    interaction_type = Column(String(255))
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="interactions")
    character = relationship("Character", back_populates="interactions")