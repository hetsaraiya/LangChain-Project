from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import random

from apis.models import Session, Question

async def get_user_session(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(Session).filter(Session.user_id == user_id)
    )
    return result.scalars().first()

async def create_session(db: AsyncSession, user_id: int):
    session = Session(user_id=user_id, session_token=f"{random.randint(1, 999999)}")
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session

async def get_session_by_id(db: AsyncSession, session_id: int):
    result = await db.execute(
        select(Session).filter(Session.id == session_id)
    )
    return result.scalars().first()

async def create_question(db: AsyncSession, question: str, answer: str, session_id: int):
    db_question = Question(
        question=question,
        answer=answer,
        session_id=session_id
    )
    db.add(db_question)
    await db.commit()
    await db.refresh(db_question)
    return db_question