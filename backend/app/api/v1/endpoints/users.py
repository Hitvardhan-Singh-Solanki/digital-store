from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from api.v1.schemas.user import UserCreate, UserDeleteRequest, UserResponse
from models.users import User
from db.session import get_db
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = pwd_context.hash(user.password)
    new_user = User(username=user.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login successful", "user_id": user.id}


@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: str, request: UserDeleteRequest, db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not pwd_context.verify(request.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid password")

    db.delete(user)
    db.commit()
    return
