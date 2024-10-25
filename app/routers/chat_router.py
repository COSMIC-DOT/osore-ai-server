from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.chat_request import ChatRequestBase
from app.services.chat_service import get_chat
from database import get_db

router = APIRouter(prefix="/api")


@router.post("/chat")
async def chat(request: ChatRequestBase, db: Session = Depends(get_db)):
    return await get_chat(chat=request.chat, room_id=request.room_id, db=db)
