# app/models/messages.py
from sqlalchemy import JSON, Column, DateTime, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class Message(BaseModel):
    __tablename__ = "messages"

    role = Column(String(50))
    content = Column(String(2000))
    timestamp = Column(DateTime, index=True)
    relevance = Column(Float, default=1.0)
    user_id = Column(String(36), ForeignKey('users.user_id'), index=True)
    adaptive_traits = Column(JSON, nullable=True)
    
    user = relationship("User", back_populates="messages")
    feedbacks = relationship("Feedback", back_populates="message")