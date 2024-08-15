# app/services/entity_manager.py

import logging
from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.entity import Entity
from app.services.db.database_setup import get_db

class EntityManager:
    def __init__(self):
        self.db: Session = next(get_db())

    def create_entity(self, entity_name: str, conversation_intent_id: int) -> Optional[Entity]:
        try:
            new_entity = Entity(entity_name=entity_name, conversation_intent_id=conversation_intent_id)
            self.db.add(new_entity)
            self.db.commit()
            self.db.refresh(new_entity)
            return new_entity
        except Exception as e:
            logging.error(f"Error creating Entity: {str(e)}")
            self.db.rollback()
            return None

    def get_entity_by_id(self, entity_id: int) -> Optional[Entity]:
        try:
            return self.db.query(Entity).filter(Entity.id == entity_id).first()
        except Exception as e:
            logging.error(f"Error getting Entity by ID: {str(e)}")
            return None

    def update_entity(self, entity_id: int, entity_name: Optional[str] = None, conversation_intent_id: Optional[int] = None) -> Optional[Entity]:
        try:
            entity = self.get_entity_by_id(entity_id)
            if entity:
                if entity_name is not None:
                    entity.entity_name = entity_name
                if conversation_intent_id is not None:
                    entity.conversation_intent_id = conversation_intent_id
                self.db.commit()
                self.db.refresh(entity)
            return entity
        except Exception as e:
            logging.error(f"Error updating Entity: {str(e)}")
            self.db.rollback()
            return None

    def delete_entity(self, entity_id: int) -> bool:
        try:
            entity = self.get_entity_by_id(entity_id)
            if entity:
                self.db.delete(entity)
                self.db.commit()
                return True
            return False
        except Exception as e:
            logging.error(f"Error deleting Entity: {str(e)}")
            self.db.rollback()
            return False

    def get_all_entities(self) -> List[Entity]:
        try:
            return self.db.query(Entity).all()
        except Exception as e:
            logging.error(f"Error getting all Entities: {str(e)}")
            return []