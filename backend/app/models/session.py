# app/models/session.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class Session(BaseModel):
    __tablename__ = "sessions"

    user_id = Column(String(36), ForeignKey("users.user_id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    status = Column(String(50), nullable=False)

    user = relationship("User", back_populates="sessions")
    messages = relationship("Message", back_populates="session")
    feedbacks = relationship("Feedback", back_populates="session")  # Add this line