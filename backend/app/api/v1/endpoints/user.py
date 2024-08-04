from fastapi import APIRouter, Depends, HTTPException
from app.core.security import get_current_user
from app.schemas.schemas import UserCreate, UserRead
from app.models.user import User
from app.services.user.user_manager import UserManager

router = APIRouter()
user_manager = UserManager()

@router.get("/me", response_model=UserRead)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: str, current_user: User = Depends(get_current_user)):
    user = user_manager.get_user_by_id(user_id)
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: str, user_update: UserCreate, current_user: User = Depends(get_current_user)):
    if current_user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this user")
    updated_user = user_manager.update_user(user_id, user_update.username, user_update.email, user_update.password)
    if updated_user:
        return updated_user
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.delete("/{user_id}")
def delete_user(user_id: str, current_user: User = Depends(get_current_user)):
    if current_user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this user")
    deleted = user_manager.delete_user(user_id)
    if deleted:
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")