from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession
from apis.db import get_db
from apis.models import User
from apis.token_gen import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_token(token, credentials_exception)

    user_query = sqlalchemy.select(User).where(User.email == token.email)
    result = await db.execute(user_query)
    user = result.scalars().first()
    if user is None:
        raise credentials_exception
    return user

from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():

    @staticmethod
    def bcrypt(password: str):
        return pwd_cxt.hash(password)
    
    @staticmethod
    def verify(hashed_password,plain_password):
        return pwd_cxt.verify(plain_password,hashed_password)