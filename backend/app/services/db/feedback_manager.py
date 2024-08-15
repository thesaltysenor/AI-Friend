# app/services/db/feedback_manager.py

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.feedback import Feedback

class FeedbackManager:
    def __init__(self, db: Session):
        self.db = db

    def create_feedback(self, user_id: str, session_id: int, message_id: str, rating: int) -> Feedback:
        db_feedback = Feedback(
            user_id=user_id,
            session_id=session_id,
            message_id=message_id,
            rating=rating
        )
        self.db.add(db_feedback)
        self.db.commit()
        self.db.refresh(db_feedback)
        return db_feedback
    
    def get_feedback_by_id(self, feedback_id: int) -> Optional[Feedback]:
        return self.db.query(Feedback).filter(Feedback.id == feedback_id).first()

    def update_feedback(self, feedback: Feedback, **kwargs) -> Optional[Feedback]:
        for key, value in kwargs.items():
            if hasattr(feedback, key):
                setattr(feedback, key, value)
        self.db.commit()
        self.db.refresh(feedback)
        return feedback

    def delete_feedback(self, feedback: Feedback) -> None:
        self.db.delete(feedback)
        self.db.commit()

    def get_all_feedback(self) -> List[Feedback]:
        return self.db.query(Feedback).all()