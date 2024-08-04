# app/models/messages.py
import time
from sqlalchemy import JSON, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.services.db.base import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String(50))
    content = Column(String(2000))
    timestamp: float = time.time()
    relevance = Column(Float, default=1.0)
    user_id = Column(String(36), ForeignKey('users.user_id'))
    adaptive_traits = Column(JSON, nullable=True)
    
    user = relationship("User", back_populates="messages")
    feedbacks = relationship("Feedback", back_populates="message")
