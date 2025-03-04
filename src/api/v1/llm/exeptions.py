from fastapi import HTTPException

class LLMExceptions:
    class InternalServerError(HTTPException):
        def __init__(self, detail: str = "Ошибка с OpenAI"):
            super().__init__(status_code=500, detail=detail)
        
    class BadRequest(HTTPException):
        def __init__(self, detail: str = "Ошибка в запросе"):
            super().__init__(status_code=400, detail=detail)
