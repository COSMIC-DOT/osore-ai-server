from sqlalchemy.orm import Session

from app.models.chat import Chat


def get_chats_by_room_id(db: Session, room_id: int):
    return db.query(Chat).filter(Chat.chatting_room_id == room_id).all()