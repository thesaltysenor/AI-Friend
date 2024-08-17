# app/api/v1/endpoints/conversation_intent.py

from fastapi import APIRouter, HTTPException, Depends, status
from app.schemas.schemas import ConversationIntentCreate, ConversationIntentRead, ConversationIntentUpdate
from app.services.db.conversation_intent_manager import ConversationIntentManager
from app.services.nlp.user_input_analyzer import UserInputAnalyzer
from app.core.dependencies import get_db
from sqlalchemy.orm import Session

router = APIRouter()

CONVERSATION_INTENT_NOT_FOUND = "Conversation Intent not found"

def get_conversation_intent_manager(db: Session = Depends(get_db)):
    return ConversationIntentManager(db)

def get_user_input_analyzer():
    return UserInputAnalyzer()

@router.post("", response_model=ConversationIntentRead, status_code=status.HTTP_201_CREATED)
def create_conversation_intent(conversation_intent: ConversationIntentCreate, conversation_intent_manager: ConversationIntentManager = Depends(get_conversation_intent_manager)):
    created_conversation_intent = conversation_intent_manager.create_conversation_intent(
        conversation_intent_name=conversation_intent.conversation_intent_name,
        description=conversation_intent.description
    )
    if not created_conversation_intent:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create Conversation Intent")
    return created_conversation_intent

@router.get("/{conversation_intent_id}", response_model=ConversationIntentRead)
def get_conversation_intent(conversation_intent_id: int, conversation_intent_manager: ConversationIntentManager = Depends(get_conversation_intent_manager)):
    conversation_intent = conversation_intent_manager.get_conversation_intent_by_id(conversation_intent_id)
    if not conversation_intent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=CONVERSATION_INTENT_NOT_FOUND)
    return conversation_intent

@router.put("/{conversation_intent_id}", response_model=ConversationIntentRead)
def update_conversation_intent(conversation_intent_id: int, conversation_intent_update: ConversationIntentUpdate, conversation_intent_manager: ConversationIntentManager = Depends(get_conversation_intent_manager)):
    updated_conversation_intent = conversation_intent_manager.update_conversation_intent(
        conversation_intent_id=conversation_intent_id,
        conversation_intent_name=conversation_intent_update.conversation_intent_name,
        description=conversation_intent_update.description
    )
    if not updated_conversation_intent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=CONVERSATION_INTENT_NOT_FOUND)
    return updated_conversation_intent

@router.delete("/{conversation_intent_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_conversation_intent(conversation_intent_id: int, conversation_intent_manager: ConversationIntentManager = Depends(get_conversation_intent_manager)):
    deleted = conversation_intent_manager.delete_conversation_intent(conversation_intent_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=CONVERSATION_INTENT_NOT_FOUND)

@router.post("/analyze")
async def analyze_user_input(user_input: str, user_input_analyzer: UserInputAnalyzer = Depends(get_user_input_analyzer)):
    try:
        conversation_intent = await user_input_analyzer.categorize_input(user_input)
        return {"conversation_intent": conversation_intent}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to analyze user input: {str(e)}")