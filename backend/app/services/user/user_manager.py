from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.schemas import UserCreate
from app.core.security import get_password_hash, verify_password

class UserManager:
    def create_user(self, db: Session, user: UserCreate):
        db_user = User(username=user.username, email=user.email, hashed_password=user.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def get_user_by_username(self, db: Session, username: str):
        return db.query(User).filter(User.username == username).first()

    def get_user_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    def authenticate_user(self, db: Session, username: str, password: str):
        user = self.get_user_by_username(db, username)
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        return user

    def update_user(self, db: Session, user_id: str, username: str, email: str, password: str):
        user = db.query(User).filter(User.user_id == user_id).first()
        if user:
            user.username = username
            user.email = email
            user.hashed_password = get_password_hash(password)
            db.commit()
            db.refresh(user)
        return user

    def delete_user(self, db: Session, user_id: str):
        user = db.query(User).filter(User.user_id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
            return True
        return False