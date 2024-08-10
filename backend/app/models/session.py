# app/models/session.py
from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from app.services.db.database import Base
from datetime import datetime

class Session(Base):
    __tablename__ = "sessions"  # Changed from "session" to "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(36), ForeignKey('users.user_id'))
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)
    status = Column(String(50))

    user = relationship("User", back_populates="sessions")
    feedbacks = relationship("Feedback", back_populates="session")