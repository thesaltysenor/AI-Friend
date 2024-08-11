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
        raise HTTPException(status_code=404, detail=USER_PREFERENCE_NOT_FOUND)