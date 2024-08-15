# app/models/feedback.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class Feedback(BaseModel):
    __tablename__ = "feedbacks"

    user_id = Column(String(36), ForeignKey('users.user_id'))
    session_id = Column(ForeignKey('sessions.id'))
    message_id = Column(ForeignKey('messages.id'))
    rating = Column(Integer)

    user = relationship("User", back_populates="feedbacks")
    session = relationship("Session", back_populates="feedbacks")
    message = relationship("Message", back_populates="feedbacks")