# app/models/feedback.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.services.db.database import Base

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(36), ForeignKey('users.user_id'))
    session_id = Column(Integer, ForeignKey('session.id'))
    message_id = Column(Integer, ForeignKey('messages.id'))
    rating = Column(Integer)

    user = relationship("User", back_populates="feedbacks")
    session = relationship("Session", back_populates="feedbacks")
    message = relationship("Message", back_populates="feedbacks")