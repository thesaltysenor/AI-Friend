# app/models/messages.py
from sqlalchemy import JSON, Column, DateTime, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.services.db.database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String(50))
    content = Column(String(2000))
    timestamp = Column(DateTime, index=True)
    relevance = Column(Float, default=1.0)
    user_id = Column(String(36), ForeignKey('users.user_id'), index=True)
    adaptive_traits = Column(JSON, nullable=True)
    
    user = relationship("User", back_populates="messages")
    feedbacks = relationship("Feedback", back_populates="message")
