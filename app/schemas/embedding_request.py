from pydantic import BaseModel


class EmbeddingRequest(BaseModel):
    repository_url: str
    room_id: int
