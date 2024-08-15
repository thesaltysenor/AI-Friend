# app/services/db/session_manager.py

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.session import Session as SessionModel
from datetime import datetime

class SessionManager:
    def __init__(self, db: Session):
        self.db = db

    def create_session(self, user_id: str, status: str) -> SessionModel:
        db_session = SessionModel(
            user_id=user_id,
            status=status,
            start_time=datetime.utcnow()
        )
        self.db.add(db_session)
        self.db.commit()
        self.db.refresh(db_session)
        return db_session

    def get_session_by_id(self, session_id: int) -> Optional[SessionModel]:
        return self.db.query(SessionModel).filter(SessionModel.id == session_id).first()

    def update_session(self, session_id: int, **kwargs) -> Optional[SessionModel]:
        db_session = self.get_session_by_id(session_id)
        if db_session:
            for key, value in kwargs.items():
                if hasattr(db_session, key):
                    setattr(db_session, key, value)
            self.db.commit()
            self.db.refresh(db_session)
        return db_session

    def delete_session(self, session_id: int) -> bool:
        db_session = self.get_session_by_id(session_id)
        if db_session:
            self.db.delete(db_session)
            self.db.commit()
            return True
        return False

    def get_sessions_by_user_id(self, user_id: str) -> List[SessionModel]:
        return self.db.query(SessionModel).filter(SessionModel.user_id == user_id).all()

    def get_all_sessions(self) -> List[SessionModel]:
        return self.db.query(SessionModel).all()

    def end_session(self, session_id: int) -> Optional[SessionModel]:
        return self.update_session(session_id, end_time=datetime.utcnow(), status="ended")