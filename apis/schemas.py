from pydantic import BaseModel, EmailStr



class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone_number: int

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

class TokenData(BaseModel):
    email: str = None

    class Config:
        orm_mode = True

class QuestionCreate(BaseModel):
    question: str
    session_id: int = None

class QuestionResponse(BaseModel):
    id: int
    question: str
    answer: str

    class Config:
        orm_mode = True