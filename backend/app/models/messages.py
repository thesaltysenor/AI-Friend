# app/models/messages.py

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import BaseModel

class Message(BaseModel):
    __tablename__ = "messages"

    id = Column(String(36), primary_key=True, index=True)
    role = Column(String(50), nullable=False)
    content = Column(String(2000), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    relevance = Column(Float, default=1.0)
    user_id = Column(String(36), ForeignKey('users.user_id'), nullable=False)
    session_id = Column(Integer, ForeignKey('sessions.id'), nullable=False)

    user = relationship("User", back_populates="messages")
    session = relationship("Session", back_populates="messages")
    feedbacks = relationship("Feedback", back_populates="message")