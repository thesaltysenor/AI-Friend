# app/api/v1/endpoints/session.py

from fastapi import APIRouter, HTTPException, Depends, status
from app.schemas.schemas import SessionCreate, SessionRead, SessionUpdate
from app.services.db.session_manager import SessionManager
from app.core.dependencies import get_db
from sqlalchemy.orm import Session

router = APIRouter()

SESSION_NOT_FOUND = "Session not found"

def get_session_manager(db: Session = Depends(get_db)):
    return SessionManager(db)

@router.post("", response_model=SessionRead, status_code=status.HTTP_201_CREATED)
def create_session(session: SessionCreate, session_manager: SessionManager = Depends(get_session_manager)):
    created_session = session_manager.create_session(session.user_id, session.status)
    if not created_session:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create Session")
    return created_session

@router.get("/{session_id}", response_model=SessionRead)
def get_session(session_id: int, session_manager: SessionManager = Depends(get_session_manager)):
    session = session_manager.get_session_by_id(session_id)
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=SESSION_NOT_FOUND)
    return session

@router.put("/{session_id}", response_model=SessionRead)
def update_session(session_id: int, session_update: SessionUpdate, session_manager: SessionManager = Depends(get_session_manager)):
    updated_session = session_manager.update_session(session_id, session_update.end_time, session_update.status)
    if not updated_session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=SESSION_NOT_FOUND)
    return updated_session

@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(session_id: int, session_manager: SessionManager = Depends(get_session_manager)):
    deleted = session_manager.delete_session(session_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=SESSION_NOT_FOUND)