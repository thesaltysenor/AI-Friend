from fastapi import APIRouter, HTTPException
from app.schemas.schemas import SessionCreate, SessionRead, SessionUpdate
from app.services.db.session_manager import SessionManager

router = APIRouter()
session_manager = SessionManager()

@router.post("", response_model=SessionRead)
def create_session(session: SessionCreate):
    created_session = session_manager.create_session(session.user_id, session.status)
    if created_session:
        return created_session
    else:
        raise HTTPException(status_code=500, detail="Failed to create Session")

@router.get("/{session_id}", response_model=SessionRead)
def get_session(session_id: int):
    session = session_manager.get_session_by_id(session_id)
    if session:
        return session
    else:
        raise HTTPException(status_code=404, detail="Session not found")

@router.put("/{session_id}", response_model=SessionRead)
def update_session(session_id: int, session_update: SessionUpdate):
    updated_session = session_manager.update_session(session_id, session_update.end_time, session_update.status)
    if updated_session:
        return updated_session
    else:
        raise HTTPException(status_code=404, detail="Session not found")

@router.delete("/{session_id}")
def delete_session(session_id: int):
    deleted = session_manager.delete_session(session_id)
    if deleted:
        return {"message": "Session deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Session not found")