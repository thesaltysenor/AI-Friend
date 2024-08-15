# app/models/user_preference.py
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class UserPreference(BaseModel):
    __tablename__ = "user_preferences"

    user_id = Column(String(36), ForeignKey('users.user_id'))
    preference_type = Column(String(255))
    preference_value = Column(String(255))

    user = relationship("User", back_populates="preferences")