from fastapi import APIRouter
from .service import llm_service
from .schemas import LLMResponse, LLMRequest

router = APIRouter(prefix="/llm", tags=["LLM"])

@router.post("/response", response_model=LLMResponse)
async def get_response(message: LLMRequest):
    return await llm_service.get_response(message)

