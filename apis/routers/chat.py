import random
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete


from apis.db import get_db
from apis.schemas import QuestionCreate, QuestionResponse
from apis.models import Session, User, Question
from app.handle_llm import get_chain
from apis.auth import get_current_user
from utils.utils import generate_title
from app.handle_llm import llm
router = APIRouter()
@router.post("/chat/query/", response_model=QuestionResponse)
async def query_llm(question: QuestionCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Handle a chat query by interacting with the language model and storing the response in the database.

    Args:
        question (QuestionCreate): The question data provided by the user.
        db (AsyncSession): The database session for executing queries.
        current_user (User): The current authenticated user making the request.

    Returns:
        QuestionResponse: The database entry of the question and its response.
    """
    try:
        result = await db.execute(
            select(Session).filter(Session.user_id == current_user.id)
        )
        session = result.scalars().first()

        if not question.session_id:
            session = Session(user_id=current_user.id, session_token=f"{random.randint(1, 999999)}", title=(await generate_title(query=question.question, llm=llm)))
            db.add(session)
            await db.commit()
            await db.refresh(session)
        else:
            result = await db.execute(
                select(Session).filter(Session.id == question.session_id)
            )
            session = result.scalars().first()

        response_content = await get_chain(question.question, db=db, session_id=session.id)

        db_question = Question(
            question=question.question,
            answer=response_content,
            session_id=session.id,
        )
        db.add(db_question)
        await db.commit()
        await db.refresh(db_question)

        return db_question
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    
@router.delete("/chat/session/{session_id}", response_model=dict)
async def delete_session(session_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Delete a chat session and all associated questions from the database.

    Args:
        session_id (int): The ID of the session to delete.
        db (AsyncSession): The database session for executing queries.
        current_user (User): The current authenticated user making the request.

    Returns:
        dict: A message indicating the session was deleted.
    """
    try:
        print(session_id)
        result = await db.execute(
            select(Session).filter(Session.id == session_id)
        )
        session = result.scalars().first()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        if not session.user_id == current_user.id:
            raise HTTPException(status_code=403, detail="Forbidden: You do not have permission to delete this session")

        await db.execute(
            delete(Question).filter(Question.session_id == session_id)
        )
        await db.execute(
            delete(Session).filter(Session.id == session_id)
        )
        await db.commit()

        return {"message": "Session and all associated questions deleted successfully"}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")