from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from apis.db import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    phone_number = Column(Integer, nullable=False)
    tokens_available = Column(Integer, default=False)
    sessions = relationship("Session", back_populates="user")

class Session(Base):
    __tablename__ = 'session'
    id = Column(Integer, primary_key=True, index=True)
    session_token = Column(String, nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="sessions")
    questions = relationship("Question", back_populates="session")
    title = Column(String, nullable=False)

class Question(Base):
    __tablename__ = 'question'
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    session_id = Column(Integer, ForeignKey("session.id"))
    session = relationship("Session", back_populates="questions")