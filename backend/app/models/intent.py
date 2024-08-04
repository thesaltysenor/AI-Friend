# app/models/intent.py
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.services.db.base import Base

class Intent(Base):
    __tablename__ = "intent"

    id = Column(Integer, primary_key=True, index=True)
    intent_name = Column(String(100), index=True)
    description = Column(Text)

    entities = relationship("Entity", back_populates="intent")