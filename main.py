from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apis.routers import login
from apis.routers import user
from apis.routers import chat
from utils.exceptions import (
    AIHostUnavailable, ai_host_unavailable,
    APILimitExceeded, api_limit_exceeded_handler,
    CannotGetContext, cannot_get_context_handler,
    LLMError, llm_error_handler,
    CrudError, crud_error_handler
)

app = FastAPI()

origins = [
    "http://192.168.3.71:5173",
    "http://localhost:5173",
    "http://localhost:3000"
]

app.add_exception_handler(AIHostUnavailable, ai_host_unavailable)
app.add_exception_handler(APILimitExceeded, api_limit_exceeded_handler)
app.add_exception_handler(CannotGetContext, cannot_get_context_handler)
app.add_exception_handler(LLMError, llm_error_handler)
app.add_exception_handler(CrudError, crud_error_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(login.router)
app.include_router(chat.router)
