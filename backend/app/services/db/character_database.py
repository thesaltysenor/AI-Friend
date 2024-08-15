# app/services/db/character_database.py

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.character import Character
from app.services.characters.character_details import CHARACTER_DETAILS

class CharacterDatabase:
    def __init__(self, db: Session):
        self.db = db

    def create_character(self, name: str, description: str, personality_traits: str, character_type: str = "default", available: bool = True) -> Character:
        db_character = Character(
            name=name,
            description=description,
            personality_traits=personality_traits,
            character_type=character_type,
            available=available
        )
        self.db.add(db_character)
        self.db.commit()
        self.db.refresh(db_character)
        return db_character
    
    def get_character_by_id(self, character_id: int) -> Optional[Character]:
        return self.db.query(Character).filter(Character.id == character_id).first()

    def update_character(self, character_id: int, **kwargs) -> Optional[Character]:
        db_character = self.get_character_by_id(character_id)
        if db_character:
            for key, value in kwargs.items():
                if hasattr(db_character, key):
                    setattr(db_character, key, value)
            self.db.commit()
            self.db.refresh(db_character)
        return db_character

    def delete_character(self, character_id: int) -> bool:
        db_character = self.get_character_by_id(character_id)
        if db_character:
            self.db.delete(db_character)
            self.db.commit()
            return True
        return False

    def get_all_characters(self) -> List[Character]:
        return self.db.query(Character).all()

    def get_default_character(self) -> Character:
        default_character = self.db.query(Character).filter(Character.character_type == "default").first()
        if not default_character:
            default_character = self.create_character(
                name="Default Character",
                description="A friendly AI assistant",
                personality_traits="Helpful, friendly, knowledgeable",
                character_type="default",
                available=True
            )
        return default_character

    def insert_or_update_character(self, character_type: str, details: dict) -> None:
        existing_character = self.db.query(Character).filter(Character.character_type == character_type).first()
        if existing_character:
            self.update_character(
                existing_character.id,
                name=details['name'],
                description=details['backstory'],
                personality_traits=', '.join(details['personality_traits']),
                available=True
            )
        else:
            self.create_character(
                name=details['name'],
                description=details['backstory'],
                personality_traits=', '.join(details['personality_traits']),
                character_type=character_type,
                available=True
            )

    def populate_characters(self) -> None:
        for character_type, details in CHARACTER_DETAILS.items():
            self.insert_or_update_character(character_type, details)

    def get_or_create_default_character(self) -> int:
        default_character = self.db.query(Character).filter(
            or_(Character.character_type == "adaptive", Character.character_type == "default")
        ).first()
        
        if default_character:
            return default_character.id
        
        new_character = self.create_character(
            name="Adaptive AI Friend",
            description="I'm an AI Friend that adapts my personality based on our conversation.",
            personality_traits="Adaptive, Observant, Evolving",
            character_type="adaptive",
            available=True
        )
        return new_character.id