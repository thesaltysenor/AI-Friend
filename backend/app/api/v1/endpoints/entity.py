from fastapi import APIRouter, HTTPException
from app.schemas.schemas import EntityCreate, EntityRead, EntityUpdate
from app.services.db.entity_manager import EntityManager

router = APIRouter()
entity_manager = EntityManager()

# Define the constant for the error message
ENTITY_NOT_FOUND = "Entity not found"

@router.post("", response_model=EntityRead)
def create_entity(entity: EntityCreate):
    created_entity = entity_manager.create_entity(entity.entity_name, entity.intent_id)
    if created_entity:
        return created_entity
    else:
        raise HTTPException(status_code=500, detail="Failed to create Entity")

@router.get("/{entity_id}", response_model=EntityRead)
def get_entity(entity_id: int):
    entity = entity_manager.get_entity_by_id(entity_id)
    if entity:
        return entity
    else:
        raise HTTPException(status_code=404, detail=ENTITY_NOT_FOUND)

@router.put("/{entity_id}", response_model=EntityRead)
def update_entity(entity_id: int, entity_update: EntityUpdate):
    updated_entity = entity_manager.update_entity(entity_id, entity_update.entity_name, entity_update.intent_id)
    if updated_entity:
        return updated_entity
    else:
        raise HTTPException(status_code=404, detail=ENTITY_NOT_FOUND)

@router.delete("/{entity_id}")
def delete_entity(entity_id: int):
    deleted = entity_manager.delete_entity(entity_id)
    if deleted:
        return {"message": "Entity deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail=ENTITY_NOT_FOUND)