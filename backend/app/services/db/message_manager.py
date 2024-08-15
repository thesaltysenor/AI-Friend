# app/services/db/message_manager.py

from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.messages import Message

class MessageManager:
    def __init__(self, db: Session):
        self.db = db

    def create_message(self, role: str, content: str, user_id: str, timestamp: datetime, relevance: float = 1.0, adaptive_traits: dict = None) -> Message:
        db_message = Message(
            role=role,
            content=content,
            user_id=user_id,
            timestamp=timestamp,
            relevance=relevance,
            adaptive_traits=adaptive_traits
        )
        self.db.add(db_message)
        self.db.commit()
        self.db.refresh(db_message)
        return db_message

    def get_message_by_id(self, message_id: int) -> Optional[Message]:
        return self.db.query(Message).filter(Message.id == message_id).first()

    def update_message(self, message_id: int, **kwargs) -> Optional[Message]:
        db_message = self.get_message_by_id(message_id)
        if db_message:
            for key, value in kwargs.items():
                if hasattr(db_message, key):
                    setattr(db_message, key, value)
            self.db.commit()
            self.db.refresh(db_message)
        return db_message

    def delete_message(self, message_id: int) -> bool:
        db_message = self.get_message_by_id(message_id)
        if db_message:
            self.db.delete(db_message)
            self.db.commit()
            return True
        return False

    def get_messages_by_user_id(self, user_id: str) -> List[Message]:
        return self.db.query(Message).filter(Message.user_id == user_id).all()

    def get_all_messages(self) -> List[Message]:
        return self.db.query(Message).all()