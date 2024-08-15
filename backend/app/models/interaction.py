# app/models/interaction.py
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel
from datetime import datetime

class Interaction(BaseModel):
    __tablename__ = "interactions"

    user_id = Column(String(36), ForeignKey('users.user_id'))
    character_id = Column(ForeignKey('characters.id'))
    interaction_type = Column(String(255))
    timestamp = Column(datetime, default=datetime.utcnow)

    user = relationship("User", back_populates="interactions")
    character = relationship("Character", back_populates="interactions")