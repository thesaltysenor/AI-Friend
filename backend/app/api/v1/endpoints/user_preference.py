from fastapi import APIRouter, HTTPException
from app.schemas.schemas import UserPreferenceCreate, UserPreferenceRead, UserPreferenceUpdate
from app.services.db.user_preference_manager import UserPreferenceManager

router = APIRouter()
user_preference_manager = UserPreferenceManager()

# Define the constant for the error message
USER_PREFERENCE_NOT_FOUND = "User Preference not found"

@router.post("", response_model=UserPreferenceRead)
def create_user_preference(user_preference: UserPreferenceCreate):
    created_user_preference = user_preference_manager.create_user_preference(user_preference.user_id, user_preference.preference_type, user_preference.preference_value)
    if created_user_preference:
        return created_user_preference
    else:
        raise HTTPException(status_code=500, detail="Failed to create User Preference")

@router.get("/{user_preference_id}", response_model=UserPreferenceRead)
def get_user_preference(user_preference_id: int):
    user_preference = user_preference_manager.get_user_preference_by_id(user_preference_id)
    if user_preference:
        return user_preference
    else:
        raise HTTPException(status_code=404, detail=USER_PREFERENCE_NOT_FOUND)

@router.put("/{user_preference_id}", response_model=UserPreferenceRead)
def update_user_preference(user_preference_id: int, user_preference_update: UserPreferenceUpdate):
    updated_user_preference = user_preference_manager.update_user_preference(user_preference_id, user_preference_update.preference_value)
    if updated_user_preference:
        return updated_user_preference
    else:
        raise HTTPException(status_code=404, detail=USER_PREFERENCE_NOT_FOUND)

@router.delete("/{user_preference_id}")
def delete_user_preference(user_preference_id: int):
    deleted = user_preference_manager.delete_user_preference(user_preference_id)
    if deleted:
        return {"message": "User Preference deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail=USER_PREFERENCE_NOT_FOUND)# app/api/v1/endpoints/user_preference.py

from fastapi import APIRouter, HTTPException, Depends, status
from app.schemas.schemas import UserPreferenceCreate, UserPreferenceRead, UserPreferenceUpdate
from app.services.db.user_preference_manager import UserPreferenceManager
from app.core.dependencies import get_db
from sqlalchemy.orm import Session

router = APIRouter()

USER_PREFERENCE_NOT_FOUND = "User Preference not found"

def get_user_preference_manager(db: Session = Depends(get_db)):
    return UserPreferenceManager(db)

@router.post("", response_model=UserPreferenceRead, status_code=status.HTTP_201_CREATED)
def create_user_preference(user_preference: UserPreferenceCreate, user_preference_manager: UserPreferenceManager = Depends(get_user_preference_manager)):
    created_user_preference = user_preference_manager.create_user_preference(user_preference.user_id, user_preference.preference_type, user_preference.preference_value)
    if not created_user_preference:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create User Preference")
    return created_user_preference

@router.get("/{user_preference_id}", response_model=UserPreferenceRead)
def get_user_preference(user_preference_id: int, user_preference_manager: UserPreferenceManager = Depends(get_user_preference_manager)):
    user_preference = user_preference_manager.get_user_preference_by_id(user_preference_id)
    if not user_preference:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=USER_PREFERENCE_NOT_FOUND)
    return user_preference

@router.put("/{user_preference_id}", response_model=UserPreferenceRead)
def update_user_preference(user_preference_id: int, user_preference_update: UserPreferenceUpdate, user_preference_manager: UserPreferenceManager = Depends(get_user_preference_manager)):
    updated_user_preference = user_preference_manager.update_user_preference(user_preference_id, user_preference_update.preference_value)
    if not updated_user_preference:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=USER_PREFERENCE_NOT_FOUND)
    return updated_user_preference

@router.delete("/{user_preference_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_preference(user_preference_id: int, user_preference_manager: UserPreferenceManager = Depends(get_user_preference_manager)):
    deleted = user_preference_manager.delete_user_preference(user_preference_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=USER_PREFERENCE_NOT_FOUND)