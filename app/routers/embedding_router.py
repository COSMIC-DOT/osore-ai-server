from fastapi import APIRouter

from app.schemas.embedding_request import EmbeddingRequest
from app.services.embedding_service import get_embedding

router = APIRouter(prefix="/api")


@router.post("/embedding")
async def embedding(embedding_request: EmbeddingRequest):
    await get_embedding(repository_url=embedding_request.repository_url, room_id=embedding_request.room_id)
