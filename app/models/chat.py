from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Chat(Base):
    __tablename__ = "chat"

    id = Column(Integer, primary_key=True, index=True)
    chat = Column(String)
    sender = Column(String)
    created_at = Column(DateTime)
    room_id = Column(Integer)
