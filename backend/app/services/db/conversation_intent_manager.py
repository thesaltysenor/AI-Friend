# app/services/db/conversation_intent_manager.py

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.conversation_intent import ConversationIntent

class ConversationIntentManager:
    def __init__(self, db: Session):
        self.db = db

    def create_conversation_intent(self, conversation_intent_name: str, description: str) -> ConversationIntent:
        db_conversation_intent = ConversationIntent(conversation_intent_name=conversation_intent_name, description=description)
        self.db.add(db_conversation_intent)
        self.db.commit()
        self.db.refresh(db_conversation_intent)
        return db_conversation_intent

    def get_conversation_intent_by_id(self, conversation_intent_id: int) -> Optional[ConversationIntent]:
        return self.db.query(ConversationIntent).filter(ConversationIntent.id == conversation_intent_id).first()

    def update_conversation_intent(self, conversation_intent_id: int, **kwargs) -> Optional[ConversationIntent]:
        db_conversation_intent = self.get_conversation_intent_by_id(conversation_intent_id)
        if db_conversation_intent:
            for key, value in kwargs.items():
                if hasattr(db_conversation_intent, key):
                    setattr(db_conversation_intent, key, value)
            self.db.commit()
            self.db.refresh(db_conversation_intent)
        return db_conversation_intent

    def delete_conversation_intent(self, conversation_intent_id: int) -> bool:
        db_conversation_intent = self.get_conversation_intent_by_id(conversation_intent_id)
        if db_conversation_intent:
            self.db.delete(db_conversation_intent)
            self.db.commit()
            return True
        return False

    def get_all_conversation_intents(self) -> List[ConversationIntent]:
        return self.db.query(ConversationIntent).all()

    def get_conversation_intent_by_name(self, conversation_intent_name: str) -> Optional[ConversationIntent]:
        return self.db.query(ConversationIntent).filter(ConversationIntent.conversation_intent_name == conversation_intent_name).first()