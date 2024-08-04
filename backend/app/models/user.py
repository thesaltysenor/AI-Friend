# app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
import uuid
from app.services.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(36), unique=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(50), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)

    messages = relationship("Message", back_populates="user")
    feedbacks = relationship("Feedback", back_populates="user")
    sessions = relationship("Session", back_populates="user")
    interactions = relationship("Interaction", back_populates="user")
    preferences = relationship("UserPreference", back_populates="user")        
    generated_images = relationship("GeneratedImage", back_populates="user")
