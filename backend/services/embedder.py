import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import shutil
from datetime import datetime, timedelta


def create_vector_store(text: str, session_id: str) -> FAISS:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    chunks = splitter.split_text(text)

    # If text is too short to chunk, use it as a single chunk
    if not chunks:
        chunks = [text]

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small", api_key=os.getenv("OPENAI_API_KEY")
    )

    vector_store = FAISS.from_texts(chunks, embedding=embeddings)
    vector_store.save_local(f"vector_stores/{session_id}")

    return vector_store


def load_vector_store(session_id: str) -> FAISS:
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small", api_key=os.getenv("OPENAI_API_KEY")
    )
    return FAISS.load_local(
        f"vector_stores/{session_id}", embeddings, allow_dangerous_deserialization=True
    )


def cleanup_old_sessions(max_age_hours: int = 24):
    vector_store_dir = "vector_stores"
    if not os.path.exists(vector_store_dir):
        return

    now = datetime.now()
    for session_folder in os.listdir(vector_store_dir):
        folder_path = os.path.join(vector_store_dir, session_folder)
        # Get folder creation time
        created_at = datetime.fromtimestamp(os.path.getctime(folder_path))
        if now - created_at > timedelta(hours=max_age_hours):
            shutil.rmtree(folder_path)
