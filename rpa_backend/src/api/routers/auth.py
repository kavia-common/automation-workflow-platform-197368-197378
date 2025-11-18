from datetime import timedelta
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from src.core.security import create_access_token, get_password_hash, verify_password
from src.db.models import User
from src.db.session import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])


class SignupRequest(BaseModel):
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., min_length=6, description="User password")


class TokenResponse(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")


@router.post(
    "/signup",
    summary="User signup",
    description="Create a new user account and return an access token.",
    response_model=TokenResponse,
)
def signup(payload: SignupRequest, db: Session = Depends(get_db)) -> Any:
    # Basic check if user exists
    existing: Optional[User] = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = User(email=payload.email, hashed_password=get_password_hash(payload.password))
    db.add(user)
    db.flush()  # Obtain ID before commit due to session dependency handling commit
    token = create_access_token(subject=str(user.id))
    return TokenResponse(access_token=token)


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., description="User password")


@router.post(
    "/login",
    summary="User login",
    description="Validate credentials and return an access token.",
    response_model=TokenResponse,
)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> Any:
    user: Optional[User] = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(subject=str(user.id), expires_delta=timedelta(hours=12))
    return TokenResponse(access_token=token)
