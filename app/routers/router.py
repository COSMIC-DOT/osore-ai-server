from fastapi import APIRouter

from app.routers import chat_router, embedding_router

router = APIRouter()

router.include_router(embedding_router.router)
router.include_router(chat_router.router)