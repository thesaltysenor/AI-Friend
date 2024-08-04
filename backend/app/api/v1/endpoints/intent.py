# app/api/v1/endpoints/intent.py

from fastapi import APIRouter, HTTPException
from app.schemas.schemas import IntentCreate, IntentRead, IntentUpdate
from app.services.db.intent_manager import IntentManager
from app.services.nlp.intent_recognizer import IntentRecognizer

router = APIRouter()
intent_manager = IntentManager()
intent_recognizer = IntentRecognizer()

@router.post("", response_model=IntentRead)
def create_intent(intent: IntentCreate):
    created_intent = intent_manager.create_intent(
        intent_name=intent.intent_name,
        description=intent.description
    )
    if created_intent:
        return created_intent
    else:
        raise HTTPException(status_code=500, detail="Failed to create Intent")

@router.get("/{intent_id}", response_model=IntentRead)
def get_intent(intent_id: int):
    intent = intent_manager.get_intent_by_id(intent_id)
    if intent:
        return intent
    else:
        raise HTTPException(status_code=404, detail="Intent not found")

@router.put("/{intent_id}", response_model=IntentRead)
def update_intent(intent_id: int, intent_update: IntentUpdate):
    updated_intent = intent_manager.update_intent(
        intent_id=intent_id,
        intent_name=intent_update.intent_name,
        description=intent_update.description
    )
    if updated_intent:
        return updated_intent
    else:
        raise HTTPException(status_code=404, detail="Intent not found")

@router.delete("/{intent_id}")
def delete_intent(intent_id: int):
    deleted = intent_manager.delete_intent(intent_id)
    if deleted:
        return {"message": "Intent deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Intent not found")

@router.post("/recognize")
async def recognize_intent(user_input: str):
    try:
        intent = await intent_recognizer.recognize_intent(user_input)
        return {"intent": intent}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to recognize intent: {str(e)}")