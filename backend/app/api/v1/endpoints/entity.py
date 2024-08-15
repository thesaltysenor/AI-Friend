# app/api/v1/endpoints/entity.py

from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.schemas.schemas import EntityCreate, EntityRead, EntityUpdate
from app.services.db.entity_manager import EntityManager
from app.core.dependencies import get_db

router = APIRouter()

ENTITY_NOT_FOUND = "Entity not found"

def get_entity_manager(db: Session = Depends(get_db)):
    return EntityManager(db)

@router.post("", response_model=EntityRead, status_code=status.HTTP_201_CREATED)
def create_entity(entity: EntityCreate, entity_manager: EntityManager = Depends(get_entity_manager)):
    created_entity = entity_manager.create_entity(entity.entity_name, entity.conversation_intent_id)
    return created_entity

@router.get("/{entity_id}", response_model=EntityRead)
def get_entity(entity_id: int, entity_manager: EntityManager = Depends(get_entity_manager)):
    entity = entity_manager.get_entity_by_id(entity_id)
    if not entity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ENTITY_NOT_FOUND)
    return entity

@router.put("/{entity_id}", response_model=EntityRead)
def update_entity(entity_id: int, entity_update: EntityUpdate, entity_manager: EntityManager = Depends(get_entity_manager)):
    updated_entity = entity_manager.update_entity(entity_id, entity_name=entity_update.entity_name, conversation_intent_id=entity_update.conversation_intent_id)
    if not updated_entity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ENTITY_NOT_FOUND)
    return updated_entity

@router.delete("/{entity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_entity(entity_id: int, entity_manager: EntityManager = Depends(get_entity_manager)):
    deleted = entity_manager.delete_entity(entity_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ENTITY_NOT_FOUND)

@router.get("", response_model=List[EntityRead])
def get_all_entities(entity_manager: EntityManager = Depends(get_entity_manager)):
    return entity_manager.get_all_entities()