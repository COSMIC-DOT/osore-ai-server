import os
import shutil
import subprocess

from fastapi import HTTPException
from langchain_core.documents import Document
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma


async def get_embedding(repository_url: str, room_id: int):
    try:
        directory = f"{room_id}"
        embedding_file_path = os.path.join(directory, "chroma_store")

        if os.path.exists(directory) and os.path.exists(embedding_file_path):
            return {"message": f"Repository already exists at {directory}", "embedding_file": embedding_file_path}

        if os.path.exists(directory):
            shutil.rmtree(directory)
        subprocess.run(["git", "clone", repository_url, directory], check=True)

        documents = load_documents_from_directory(directory)
        text_splitter = CharacterTextSplitter(chunk_size=1042)
        texts = text_splitter.split_documents(documents)
        embeddings = OpenAIEmbeddings()

        vectorstore = Chroma.from_documents(texts, embeddings, persist_directory=embedding_file_path)
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail="Failed to clone repository.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to create embeddings.")


def load_documents_from_directory(directory, file_extensions=None):
    if file_extensions is None:
        file_extensions = [".md", ".txt", ".py", ".java", ".js", ".html", ".css"]

    documents = []
    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.lower().endswith(ext) for ext in file_extensions):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        documents.append(Document(page_content=content, metadata={"file_path": file_path}))
                except Exception as e:
                    print(f"Failed to read {file_path}: {e}")
    return documents
