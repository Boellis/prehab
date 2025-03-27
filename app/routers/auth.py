"""
Handles user registration, login, and token refresh endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_jwt,
)
from app.db.database import get_db
from app.db.models import User
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import Token, RefreshTokenRequest

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse)
def register_user(user_create: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user_create.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    new_user = User(
        username=user_create.username,
        hashed_password=get_password_hash(user_create.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
def login(user_create: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_create.username).first()
    if not user or not verify_password(user_create.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(subject=str(user.id))
    refresh_token = create_refresh_token(subject=str(user.id))
    return Token(access_token=access_token, refresh_token=refresh_token)

@router.post("/refresh", response_model=Token)
def refresh_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    try:
        payload = decode_jwt(request.refresh_token)
    except:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    if payload.get("scope") != "refresh_token":
        raise HTTPException(status_code=401, detail="Invalid scope for token")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    new_access_token = create_access_token(subject=str(user.id))
    new_refresh_token = create_refresh_token(subject=str(user.id))
    return Token(access_token=new_access_token, refresh_token=new_refresh_token)
