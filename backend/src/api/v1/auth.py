from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.shared.database import get_db
from src.features.auth import commands, schemas
from src.features.auth.jwt import create_access_token, get_current_user
from src.features.auth.models import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return commands.create_user(db=db, user=user)


@router.post("/login", response_model=schemas.Token)
def login(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = commands.authenticate_user(db, credentials.email, credentials.password)
    access_token = create_access_token(data={"sub": user.id})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
