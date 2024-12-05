from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy

from apis.auth import Hash
from apis.db import get_db
from apis.models import User
from apis import token_gen as token
from apis.logger import logger

router = APIRouter(tags=["Auth"])

@router.post("/login/")
async def login(request: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    try:
        query = sqlalchemy.select(User).where(User.email == request.username)
        result = await db.execute(query)
        user = result.scalars().first()

        if not user:
            raise ValueError("Invalid credentials 1")

        if not Hash.verify(user.hashed_password, request.password):
            raise ValueError(detail="Invalid credentials 2")
        
        access_token = token.create_access_token(user=user)
        refresh_token = token.create_refresh_token(user=user)
        logger.info(f"User {user.email} logged in")
        return {
            "user_name": user.name,
            "user_id": user.id,
            "user_email": user.email,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    except Exception as e:
        logger.error(f"Error: faced an {e} while logging in")
        raise HTTPException(detail=str(e), status_code=500)