from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.schemas import CharacterCreate, CharacterRead, CharacterUpdate
from app.services.db.character_database import CharacterDatabase
from app.services.characters.character_details import CHARACTER_DETAILS
from app.services.db.database_setup import get_db

router = APIRouter()

# Define the constant for the error message
CHARACTER_NOT_FOUND = "Character not found"

@router.post("", response_model=CharacterRead)
def create_character(character: CharacterCreate, db: Session = Depends(get_db)):
    character_database = CharacterDatabase(db)
    created_character = character_database.create_character(
        name=character.name,
        description=character.description,
        personality_traits=character.personality_traits,
        character_type=character.character_type,
        available=character.available
    )
    return created_character

@router.get("/{character_id}", response_model=CharacterRead)
def get_character(character_id: int, db: Session = Depends(get_db)):
    character_database = CharacterDatabase(db)
    character = character_database.get_character_by_id(character_id)
    if character is None:
        raise HTTPException(status_code=404, detail=CHARACTER_NOT_FOUND)
    return character

@router.put("/{character_id}", response_model=CharacterRead)
def update_character(character_id: int, character_update: CharacterUpdate, db: Session = Depends(get_db)):
    character_database = CharacterDatabase(db)
    updated_character = character_database.update_character(
        character_id,
        name=character_update.name,
        description=character_update.description,
        personality_traits=character_update.personality_traits,
        character_type=character_update.character_type,
        available=character_update.available
    )
    if updated_character is None:
        raise HTTPException(status_code=404, detail=CHARACTER_NOT_FOUND)
    return updated_character

@router.delete("/{character_id}")
def delete_character(character_id: int, db: Session = Depends(get_db)):
    character_database = CharacterDatabase(db)
    deleted = character_database.delete_character(character_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=CHARACTER_NOT_FOUND)
    return {"message": "Character deleted successfully"}

@router.get("", response_model=List[CharacterRead])
def get_characters(db: Session = Depends(get_db)):
    character_database = CharacterDatabase(db)
    characters = character_database.get_all_characters()
    if not characters:
        # If no characters are in the database, create them from CHARACTER_DETAILS
        for character_type, details in CHARACTER_DETAILS.items():
            character_database.create_character(
                name=character_type,
                description=details['backstory'],
                personality_traits=f"Speech style: {details['speech_style']}. Knowledge areas: {', '.join(details['knowledge_areas'])}",
                character_type=character_type,
                available=True
            )
        characters = character_database.get_all_characters()
    
    return characters