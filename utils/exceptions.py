from fastapi import Request
from fastapi.responses import JSONResponse

class AIHostUnavailable(Exception):
    def __init__(self, message="AI host is unavailable"):
        self.message = message
        super().__init__(self.message)

class APILimitExceeded(Exception):
    def __init__(self, message="API limit exceeded"):
        self.message = message
        super().__init__(self.message)

class CannotGetContext(Exception):
    def __init__(self, message="Cannot get context"):
        self.message = message
        super().__init__(self.message)

class LLMError(Exception):
    def __init__(self, message="Error in LLM"):
        self.message = message
        super().__init__(self.message)

class CrudError(Exception):
    def __init__(self, message="Error in CRUD operations"):
        self.message = message
        super().__init__(self.message)

async def ai_host_unavailable(request: Request, exc: Exception):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )

async def api_limit_exceeded_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=429,
        content={"message": str(exc)},
    )

async def cannot_get_context_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )

async def llm_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )

async def crud_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )