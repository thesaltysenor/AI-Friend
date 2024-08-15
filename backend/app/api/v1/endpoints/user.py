# app/api/v1/endpoints/user.py

from fastapi import APIRouter, Depends, HTTPException, status
from app.core.security import get_current_user
from app.schemas.schemas import UserCreate, UserRead, UserUpdate
from app.models.user import User
from app.services.db.user_manager import UserManager
from app.core.dependencies import get_db
from sqlalchemy.orm import Session

router = APIRouter()

USER_NOT_FOUND = "User not found"

def get_user_manager(db: Session = Depends(get_db)):
    return UserManager(db)

@router.get("/me", response_model=UserRead)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: str, current_user: User = Depends(get_current_user), user_manager: UserManager = Depends(get_user_manager)):
    user = user_manager.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_FOUND)
    return user

@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: str, user_update: UserUpdate, current_user: User = Depends(get_current_user), user_manager: UserManager = Depends(get_user_manager)):
    if current_user.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this user")
    updated_user = user_manager.update_user(user_id, user_update.username, user_update.email, user_update.password)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_FOUND)
    return updated_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str, current_user: User = Depends(get_current_user), user_manager: UserManager = Depends(get_user_manager)):
    if current_user.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this user")
    deleted = user_manager.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_FOUND)