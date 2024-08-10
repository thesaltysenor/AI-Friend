# app/models/user_preference.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.services.db.database import Base

class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))  # Changed from String(36) to Integer
    preference_type = Column(String(255))  # Changed from String(100) to String(255)
    preference_value = Column(String(255))

    user = relationship("User", back_populates="preferences")