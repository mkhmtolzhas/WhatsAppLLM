from fastapi import APIRouter
from .llm.router import router as llm_router

router = APIRouter(prefix="/v1")

router.include_router(llm_router, tags=["LLM"])

@router.get("/")
async def root():
    return {"message": "Hello World"}