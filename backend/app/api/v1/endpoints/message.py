from fastapi import APIRouter, HTTPException
from app.schemas.schemas import MessageCreate, MessageRead, MessageUpdate
from app.services.db.message_manager import MessageManager

router = APIRouter()
message_manager = MessageManager()

# Define the constant for the error message
MESSAGE_NOT_FOUND = "Message not found"

@router.post("", response_model=MessageRead)
def create_message(message: MessageCreate):
    created_message = message_manager.create_message(message.role, message.content, message.user_id, message.relevance)
    if created_message:
        return created_message
    else:
        raise HTTPException(status_code=500, detail="Failed to create Message")

@router.get("/{message_id}", response_model=MessageRead)
def get_message(message_id: int):
    message = message_manager.get_message_by_id(message_id)
    if message:
        return message
    else:
        raise HTTPException(status_code=404, detail=MESSAGE_NOT_FOUND)

@router.put("/{message_id}", response_model=MessageRead)
def update_message(message_id: int, message_update: MessageUpdate):
    updated_message = message_manager.update_message(message_id, message_update.role, message_update.content, message_update.relevance)
    if updated_message:
        return updated_message
    else:
        raise HTTPException(status_code=404, detail=MESSAGE_NOT_FOUND)

@router.delete("/{message_id}")
def delete_message(message_id: int):
    deleted = message_manager.delete_message(message_id)
    if deleted:
        return {"message": "Message deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail=MESSAGE_NOT_FOUND)