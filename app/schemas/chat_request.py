from pydantic import BaseModel


class ChatRequestBase(BaseModel):
    chat: str
    room_id: int
