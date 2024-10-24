import os

from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from sqlalchemy.orm import Session

from app.crud.chat_crud import get_chats_by_room_id
from fastapi import HTTPException

from langchain_chroma import Chroma


async def get_chat(chat: str, room_id: int, db: Session):
    chat_history = get_chats_by_room_id(db, room_id)
    if (chat_history is None) or (len(chat_history) == 0):
        raise HTTPException(status_code=404, detail="Chat not found.")

    directory = f"{room_id}"
    embedding_file_path = os.path.join(directory, "chroma_store")

    if not os.path.exists(embedding_file_path):
        raise HTTPException(status_code=500, detail="Embedding file not found.")

    vectorstore = Chroma(persist_directory=embedding_file_path, embedding_function=OpenAIEmbeddings())
    retriever = vectorstore.as_retriever(search_type="cosine", search_kwargs={"k": 8})

    chat_model = ChatOpenAI(model_name="gpt-4")
    conversational_chain = ConversationalRetrievalChain.from_llm(
        llm=chat_model,
        retriever=retriever,
        memory=ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    )

    answer = conversational_chain({'question': chat, 'chat_history': chat_history})
    return {"answer": answer}
