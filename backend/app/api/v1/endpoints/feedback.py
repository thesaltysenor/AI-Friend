# app/api/v1/endpoints/feedback.py

from fastapi import APIRouter, HTTPException, Depends, status
from app.schemas.schemas import FeedbackCreate, FeedbackRead, FeedbackUpdate
from app.services.db.feedback_manager import FeedbackManager
from app.core.dependencies import get_db
from sqlalchemy.orm import Session

router = APIRouter()

FEEDBACK_NOT_FOUND = "Feedback not found"

def get_feedback_manager(db: Session = Depends(get_db)):
    return FeedbackManager(db)

@router.post("", response_model=FeedbackRead, status_code=status.HTTP_201_CREATED)
def create_feedback(feedback: FeedbackCreate, feedback_manager: FeedbackManager = Depends(get_feedback_manager)):
    created_feedback = feedback_manager.create_feedback(feedback.user_id, feedback.session_id, feedback.message_id, feedback.rating)
    if not created_feedback:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create Feedback")
    return created_feedback

@router.get("/{feedback_id}", response_model=FeedbackRead)
def get_feedback(feedback_id: int, feedback_manager: FeedbackManager = Depends(get_feedback_manager)):
    feedback = feedback_manager.get_feedback_by_id(feedback_id)
    if not feedback:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=FEEDBACK_NOT_FOUND)
    return feedback

@router.put("/{feedback_id}", response_model=FeedbackRead)
def update_feedback(feedback_id: int, feedback_update: FeedbackUpdate, feedback_manager: FeedbackManager = Depends(get_feedback_manager)):
    updated_feedback = feedback_manager.update_feedback(feedback_id, feedback_update.rating)
    if not updated_feedback:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=FEEDBACK_NOT_FOUND)
    return updated_feedback

@router.delete("/{feedback_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_feedback(feedback_id: int, feedback_manager: FeedbackManager = Depends(get_feedback_manager)):
    deleted = feedback_manager.delete_feedback(feedback_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=FEEDBACK_NOT_FOUND)