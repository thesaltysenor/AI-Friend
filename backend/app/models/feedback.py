# app/models/feedback.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class Feedback(BaseModel):
    __tablename__ = "feedbacks"

    user_id = Column(String(36), ForeignKey("users.user_id"), nullable=False)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    message_id = Column(String(36), ForeignKey("messages.id"), nullable=False)
    rating = Column(Integer, nullable=False)

    user = relationship("User", back_populates="feedbacks")
    session = relationship("Session", back_populates="feedbacks")  # Add this line
    message = relationship("Message", back_populates="feedbacks")