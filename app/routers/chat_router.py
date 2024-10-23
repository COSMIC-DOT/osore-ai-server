from fastapi import APIRouter

from app.schemas.chat_request import ChatRequestBase
from app.services.chat_service import chat

router = APIRouter(prefix="/api")


@router.post("/chat")
async def chat(request: ChatRequestBase):
    return chat(request.chat, request.room_id)
