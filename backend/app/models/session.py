# app/models/session.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import BaseModel

class Session(BaseModel):
    __tablename__ = "sessions"

    user_id = Column(Integer, ForeignKey("users.id"))
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    status = Column(String(50))

    user = relationship("User", back_populates="sessions")
    messages = relationship("Message", back_populates="session")