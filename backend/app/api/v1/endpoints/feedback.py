from fastapi import APIRouter, HTTPException
from app.schemas.schemas import FeedbackCreate, FeedbackRead, FeedbackUpdate
from app.services.db.feedback_manager import FeedbackManager

router = APIRouter()
feedback_manager = FeedbackManager()

# Define the constant for the error message
FEEDBACK_NOT_FOUND = "Feedback not found"

@router.post("", response_model=FeedbackRead)
def create_feedback(feedback: FeedbackCreate):
    created_feedback = feedback_manager.create_feedback(feedback.user_id, feedback.session_id, feedback.message_id, feedback.rating)
    if created_feedback:
        return created_feedback
    else:
        raise HTTPException(status_code=500, detail="Failed to create Feedback")

@router.get("/{feedback_id}", response_model=FeedbackRead)
def get_feedback(feedback_id: int):
    feedback = feedback_manager.get_feedback_by_id(feedback_id)
    if feedback:
        return feedback
    else:
        raise HTTPException(status_code=404, detail=FEEDBACK_NOT_FOUND)

@router.put("/{feedback_id}", response_model=FeedbackRead)
def update_feedback(feedback_id: int, feedback_update: FeedbackUpdate):
    updated_feedback = feedback_manager.update_feedback(feedback_id, feedback_update.rating)
    if updated_feedback:
        return updated_feedback
    else:
        raise HTTPException(status_code=404, detail=FEEDBACK_NOT_FOUND)

@router.delete("/{feedback_id}")
def delete_feedback(feedback_id: int):
    deleted = feedback_manager.delete_feedback(feedback_id)
    if deleted:
        return {"message": "Feedback deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail=FEEDBACK_NOT_FOUND)