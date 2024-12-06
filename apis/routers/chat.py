from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from apis.db import get_db
from apis.schemas import QuestionCreate, QuestionResponse
from apis.models import User, Question
from app.handle_llm import get_chain_2

router = APIRouter()

@router.post("/chat/", response_model=QuestionResponse)
async def create_question(question: QuestionCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.id == question.user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_question = Question(
        question=question.question,
        answer=question.answer,
        user_id=question.user_id
    )
    db.add(db_question)
    await db.commit()
    await db.refresh(db_question)
    return db_question

@router.post("/chat/query/", response_model=QuestionResponse)
async def query_llm(question: QuestionCreate, db: AsyncSession = Depends(get_db)):
    # query = select(User).filter(User.id == question.user_id)
    # result = await db.execute(query)
    # user = result.scalars().all()
    # if not user:
    #     raise HTTPException(status_code=404, detail="User not found")
    
    response_content = await get_chain_2(question.question, user_id=question.user_id, db=db)
    
    db_question = Question(
        question=question.question,
        answer=response_content,
        user_id=question.user_id
    )
    db.add(db_question)
    await db.commit()
    await db.refresh(db_question)
    return db_question