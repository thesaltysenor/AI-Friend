from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.schemas import UserCreate
from app.core.security import get_password_hash, verify_password

class UserManager:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: UserCreate) -> User:
        hashed_password = get_password_hash(user.password)
        db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        return self.db.query(User).filter(User.user_id == user_id).first()

    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = self.get_user_by_username(username)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    def update_user(self, user_id: str, **kwargs) -> Optional[User]:
        user = self.get_user_by_id(user_id)
        if user:
            for key, value in kwargs.items():
                if key == 'password':
                    user.hashed_password = get_password_hash(value)
                elif hasattr(user, key):
                    setattr(user, key, value)
            self.db.commit()
            self.db.refresh(user)
        return user

    def delete_user(self, user_id: str) -> bool:
        user = self.get_user_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False

    def get_all_users(self) -> List[User]:
        return self.db.query(User).all()

    def is_username_taken(self, username: str) -> bool:
        return self.db.query(User).filter(User.username == username).first() is not None

    def is_email_taken(self, email: str) -> bool:
        return self.db.query(User).filter(User.email == email).first() is not None