# app/services/db/user_preference_manager.py

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.user_preference import UserPreference

class UserPreferenceManager:
    def __init__(self, db: Session):
        self.db = db

    def create_user_preference(self, user_id: int, preference_type: str, preference_value: str) -> UserPreference:
        db_user_preference = UserPreference(
            user_id=user_id,
            preference_type=preference_type,
            preference_value=preference_value
        )
        self.db.add(db_user_preference)
        self.db.commit()
        self.db.refresh(db_user_preference)
        return db_user_preference
    
    def get_user_preference_by_id(self, user_preference_id: int) -> Optional[UserPreference]:
        return self.db.query(UserPreference).filter(UserPreference.id == user_preference_id).first()

    def update_user_preference(self, user_preference: UserPreference, **kwargs) -> Optional[UserPreference]:
        for key, value in kwargs.items():
            if hasattr(user_preference, key):
                setattr(user_preference, key, value)
        self.db.commit()
        self.db.refresh(user_preference)
        return user_preference

    def delete_user_preference(self, user_preference: UserPreference) -> None:
        self.db.delete(user_preference)
        self.db.commit()

    def get_all_user_preferences(self) -> List[UserPreference]:
        return self.db.query(UserPreference).all()