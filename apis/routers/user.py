from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from apis.db import get_db
from apis.schemas import UserCreate, UserResponse
from apis.models import User
from apis.auth import Hash
from sqlalchemy import select

router = APIRouter(tags=["User"], prefix="/user")

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    stmt = select(User).where(User.email == user.email)
    db_user = await db.execute(stmt)
    db_user = db_user.scalars().first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = Hash.bcrypt(user.password)
    db_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password,
        phone_number=user.phone_number,
        tokens_available=20000
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user