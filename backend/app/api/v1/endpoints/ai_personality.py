# app/api/v1/endpoints/ai_personality.py
from typing import List
from fastapi import APIRouter, HTTPException
from app.schemas.schemas import AIPersonalityCreate, AIPersonalityRead, AIPersonalityUpdate
from app.services.db.ai_personality_manager import AIPersonalityManager
from app.services.characters.character_details import CHARACTER_DETAILS

router = APIRouter()
ai_personality_manager = AIPersonalityManager()

@router.post("", response_model=AIPersonalityRead)
def create_ai_personality(ai_personality: AIPersonalityCreate):
    created_ai_personality = ai_personality_manager.create_ai_personality(
        name=ai_personality.name,
        description=ai_personality.description,
        personality_traits=ai_personality.personality_traits,
        character_type=ai_personality.character_type,
        available=ai_personality.available
    )
    if created_ai_personality:
        return created_ai_personality
    else:
        raise HTTPException(status_code=500, detail="Failed to create AI Personality")

@router.get("/{ai_personality_id}", response_model=AIPersonalityRead)
def get_ai_personality(ai_personality_id: int):
    ai_personality = ai_personality_manager.get_ai_personality_by_id(ai_personality_id)
    if ai_personality:
        return ai_personality
    else:
        raise HTTPException(status_code=404, detail="AI Personality not found")

@router.put("/{ai_personality_id}", response_model=AIPersonalityRead)
def update_ai_personality(ai_personality_id: int, ai_personality_update: AIPersonalityUpdate):
    updated_ai_personality = ai_personality_manager.update_ai_personality(
        ai_personality_id=ai_personality_id,
        name=ai_personality_update.name,
        description=ai_personality_update.description,
        personality_traits=ai_personality_update.personality_traits,
        character_type=ai_personality_update.character_type,
        available=ai_personality_update.available
    )
    if updated_ai_personality:
        return updated_ai_personality
    else:
        raise HTTPException(status_code=404, detail="AI Personality not found")

@router.delete("/{ai_personality_id}")
def delete_ai_personality(ai_personality_id: int):
    deleted = ai_personality_manager.delete_ai_personality(ai_personality_id)
    if deleted:
        return {"message": "AI Personality deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="AI Personality not found")
    
@router.get("", response_model=List[AIPersonalityRead])
def get_all_ai_personalities():
    ai_personalities = ai_personality_manager.get_all_ai_personalities()
    if not ai_personalities:
        # If no personalities are in the database, create them from CHARACTER_DETAILS
        for character_type, details in CHARACTER_DETAILS.items():
            ai_personality_manager.create_ai_personality(
                name=character_type,
                description=details['backstory'],
                personality_traits=f"Speech style: {details['speech_style']}. Knowledge areas: {', '.join(details['knowledge_areas'])}",
                character_type=character_type,
                available=True
            )
        ai_personalities = ai_personality_manager.get_all_ai_personalities()
    
    return [AIPersonalityRead.from_orm(ap) for ap in ai_personalities]