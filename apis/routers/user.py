from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from apis.models import Question, Session as SessionChat
from apis.db import get_db
from apis.schemas import UserCreate, UserResponse
from apis.models import User
from apis.auth import Hash, get_current_user
from sqlalchemy import select

router = APIRouter(tags=["User"], prefix="/user")

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user with the provided details.

    Args:
        user (UserCreate): The user details for creating a new account.
        db (Session): The database session for executing queries.

    Returns:
        User: The newly created user object.

    Raises:
        HTTPException: If the email is already registered.
    """
    try:
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
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error {str(e)}")
    
@router.get("/chat/sessions")
async def get_user_sessions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Get all sessions for a given user.

    Args:
        user_id (int): The ID of the user.
        db (Session): The database session for executing queries.

    Returns:
        List[Session]: A list of sessions for the user.

    Raises:
        HTTPException: If the user is not found.
    """
    try:
        user = await db.get(User, current_user.id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        sessions = await db.execute(select(SessionChat).where(SessionChat.user_id == current_user.id))
        sessions = sessions.scalars().all()
        return {
            "user_id": current_user.name,
            "sessions": [
                {
                    "id": session.id,
                    "token": session.session_token,
                    "title": session.title,
                } for session in sessions
            ]
        }
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error {str(e)}")
    
@router.get("/chat/sessions/{session_id}/qa")
async def get_session_qa(session_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Get all questions and answers for a given session.

    Args:
        session_id (int): The ID of the session.
        db (Session): The database session for executing queries.

    Returns:
        List[Dict]: A list of questions and answers for the session.

    Raises:
        HTTPException: If the session is not found or does not belong to the user.
    """
    try:
        session = await db.get(SessionChat, session_id)
        if not session or session.user_id != current_user.id:
            raise HTTPException(status_code=404, detail="Session not found or access denied")
        
        qa_pairs = await db.execute(select(Question).where(Question.session_id == session_id).order_by(Question.id))
        qa_pairs = qa_pairs.scalars().all()
        return {
            "session_id": session_id,
            "qa_pairs": [
                {
                    "question": qa.question,
                    "answer": qa.answer,
                } for qa in qa_pairs
            ]
        }
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error {str(e)}")