from fastapi import APIRouter
from .llm.router import router as llm_router

router = APIRouter(prefix="/v2")

router.include_router(llm_router)

@router.get("/")
async def root():
    return {"message": "Hello World"}