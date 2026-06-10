import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


def create_vector_store(text: str, session_id: str) -> FAISS:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    chunks = splitter.split_text(text)

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=os.getenv("OPENAI_API_KEY")
    )

    vector_store = FAISS.from_texts(chunks, embedding=embeddings)
    vector_store.save_local(f"vector_stores/{session_id}")

    return vector_store


def load_vector_store(session_id: str) -> FAISS:
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    return FAISS.load_local(
        f"vector_stores/{session_id}",
        embeddings,
        allow_dangerous_deserialization=True
    )