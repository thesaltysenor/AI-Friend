# app/models/user_preference.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.services.db.database import Base

class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(36), ForeignKey('users.user_id'))
    preference_type = Column(String(100))
    preference_value = Column(String(255))

    user = relationship("User", back_populates="preferences")