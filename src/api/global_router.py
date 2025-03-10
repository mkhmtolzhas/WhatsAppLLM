from fastapi import APIRouter
from .v1.router import router as v1_router
from .v2.router import router as v2_router

router = APIRouter(prefix="/api")

router.include_router(v1_router)
router.include_router(v2_router)

@router.get("/")
async def root():
    return {"message": "Hello World"}