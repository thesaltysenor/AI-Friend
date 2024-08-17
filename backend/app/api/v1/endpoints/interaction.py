# app/api/v1/endpoints/interaction.py

from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from app.schemas.schemas import InteractionCreate, InteractionRead
from app.services.db.interaction_manager import InteractionManager
from app.services.db.character_database import CharacterDatabase
from app.core.dependencies import get_db
from sqlalchemy.orm import Session

router = APIRouter()

def get_interaction_manager(db: Session = Depends(get_db)):
    return InteractionManager(db)

def get_character_database(db: Session = Depends(get_db)):
    return CharacterDatabase(db)

@router.post("", response_model=InteractionRead, status_code=status.HTTP_201_CREATED)
def create_interaction(
    interaction: InteractionCreate,
    interaction_manager: InteractionManager = Depends(get_interaction_manager),
    character_database: CharacterDatabase = Depends(get_character_database)
):
    if interaction.character_id is None or not character_database.get_character_by_id(interaction.character_id):
        interaction.character_id = character_database.get_or_create_default_character()
    
    created_interaction = interaction_manager.create_interaction(
        user_id=interaction.user_id,
        character_id=interaction.character_id,
        interaction_type=interaction.interaction_type
    )
    if not created_interaction:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create Interaction")
    return created_interaction

@router.get("/users/{user_id}", response_model=List[InteractionRead])
def get_interactions_by_user_id(
    user_id: int,
    interaction_manager: InteractionManager = Depends(get_interaction_manager)
):
    interactions = interaction_manager.get_interactions_by_user_id(user_id)
    return interactions

@router.delete("/{interaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_interaction(
    interaction_id: int,
    interaction_manager: InteractionManager = Depends(get_interaction_manager)
):
    deleted = interaction_manager.delete_interaction(interaction_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interaction not found")