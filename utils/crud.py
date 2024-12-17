from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import random

from apis.models import Session, Question
from utils.exceptions import CrudError

async def get_user_session(db: AsyncSession, user_id: int):
    try:
        result = await db.execute(
            select(Session).filter(Session.user_id == user_id)
        )
        return result.scalars().first()
    except Exception as e:
        raise CrudError(f"Error getting user session: {str(e)}")

async def create_session(db: AsyncSession, user_id: int):
    try:
        session = Session(user_id=user_id, session_token=f"{random.randint(1, 999999)}")
        db.add(session)
        await db.commit()
        await db.refresh(session)
        return session
    except Exception as e:
        raise CrudError(f"Error creating session: {str(e)}")

async def get_session_by_id(db: AsyncSession, session_id: int):
    try:
        result = await db.execute(
            select(Session).filter(Session.id == session_id)
        )
        return result.scalars().first()
    except Exception as e:
        raise CrudError(f"Error getting session by ID: {str(e)}")

async def create_question(db: AsyncSession, question: str, answer: str, session_id: int):
    try:
        db_question = Question(
            question=question,
            answer=answer,
            session_id=session_id
        )
        db.add(db_question)
        await db.commit()
        await db.refresh(db_question)
        return db_question
    except Exception as e:
        raise CrudError(f"Error creating question: {str(e)}")