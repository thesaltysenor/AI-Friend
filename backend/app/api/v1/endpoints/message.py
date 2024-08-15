# app/api/v1/endpoints/message.py

from fastapi import APIRouter, HTTPException, Depends, status
from app.schemas.schemas import MessageCreate, MessageRead, MessageUpdate
from app.services.db.message_manager import MessageManager
from app.core.dependencies import get_db
from sqlalchemy.orm import Session

router = APIRouter()

MESSAGE_NOT_FOUND = "Message not found"

def get_message_manager(db: Session = Depends(get_db)):
    return MessageManager(db)

@router.post("", response_model=MessageRead, status_code=status.HTTP_201_CREATED)
def create_message(message: MessageCreate, message_manager: MessageManager = Depends(get_message_manager)):
    created_message = message_manager.create_message(message.role, message.content, message.user_id, message.relevance)
    if not created_message:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create Message")
    return created_message

@router.get("/{message_id}", response_model=MessageRead)
def get_message(message_id: int, message_manager: MessageManager = Depends(get_message_manager)):
    message = message_manager.get_message_by_id(message_id)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=MESSAGE_NOT_FOUND)
    return message

@router.put("/{message_id}", response_model=MessageRead)
def update_message(message_id: int, message_update: MessageUpdate, message_manager: MessageManager = Depends(get_message_manager)):
    updated_message = message_manager.update_message(message_id, message_update.role, message_update.content, message_update.relevance)
    if not updated_message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=MESSAGE_NOT_FOUND)
    return updated_message

@router.delete("/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_message(message_id: int, message_manager: MessageManager = Depends(get_message_manager)):
    deleted = message_manager.delete_message(message_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=MESSAGE_NOT_FOUND)