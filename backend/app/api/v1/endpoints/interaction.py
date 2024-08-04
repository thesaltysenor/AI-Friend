from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from app.schemas.schemas import InteractionCreate, InteractionRead
from app.services.nlp.interaction_manager import InteractionManager
from app.services.db.ai_personality_manager import AIPersonalityManager

router = APIRouter()
interaction_manager = InteractionManager()

class InteractionCreate(BaseModel):
    user_id: str
    ai_personality_id: Optional[int] = None
    interaction_type: str

@router.post("", response_model=InteractionRead)
def create_interaction(interaction: InteractionCreate):
    ai_personality_manager = AIPersonalityManager()
    
    if interaction.ai_personality_id is None or not ai_personality_manager.get_ai_personality_by_id(interaction.ai_personality_id):
        interaction.ai_personality_id = ai_personality_manager.get_or_create_default_ai_personality()
    
    created_interaction = interaction_manager.create_interaction(
        user_id=interaction.user_id,
        ai_personality_id=interaction.ai_personality_id,
        interaction_type=interaction.interaction_type
    )
    if created_interaction:
        return created_interaction
    else:
        raise HTTPException(status_code=500, detail="Failed to create Interaction")

@router.get("/users/{user_id}", response_model=List[InteractionRead])
def get_interactions_by_user_id(user_id: int):
    interactions = interaction_manager.get_interactions_by_user_id(user_id)
    return interactions

@router.delete("/{interaction_id}")
def delete_interaction(interaction_id: int):
    deleted = interaction_manager.delete_interaction(interaction_id)
    if deleted:
        return {"message": "Interaction deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Interaction not found")