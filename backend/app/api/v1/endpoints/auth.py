# app/api/v1/endpoints/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.security import create_access_token, get_current_user
from app.schemas.schemas import UserCreate, Token, UserRead
from app.services.db.user_manager import UserManager
from app.services.db.database_setup import get_db
from datetime import timedelta
from app.core.config import settings

router = APIRouter()

def get_user_manager(db: Session = Depends(get_db)):
    return UserManager(db)

@router.post("/register", response_model=Token)
def register_user(user: UserCreate, user_manager: UserManager = Depends(get_user_manager)):
    if user_manager.is_email_taken(user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    if user_manager.is_username_taken(user.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")
    
    new_user = user_manager.create_user(user)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": new_user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), user_manager: UserManager = Depends(get_user_manager)):
    user = user_manager.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserRead)
async def read_users_me(current_user_email: str = Depends(get_current_user), user_manager: UserManager = Depends(get_user_manager)):
    user = user_manager.get_user_by_email(current_user_email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user