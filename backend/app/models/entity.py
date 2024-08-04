# app/models/entity.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.services.db.base import Base

class Entity(Base):
    __tablename__ = "entity"

    id = Column(Integer, primary_key=True, index=True)
    entity_name = Column(String(100), index=True)
    intent_id = Column(Integer, ForeignKey('intent.id'))

    intent = relationship("Intent", back_populates="entities")