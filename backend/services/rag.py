import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

session_histories = {}


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def format_history(history):
    if not history:
        return "No previous conversation."
    result = ""
    for human, ai in history:
        result += f"Human: {human}\nAI: {ai}\n\n"
    return result


def ask_question(session_id: str, question: str) -> str:
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=os.getenv("OPENAI_API_KEY")
    )

    vector_store = FAISS.load_local(
        f"vector_stores/{session_id}",
        embeddings,
        allow_dangerous_deserialization=True
    )

    retriever = vector_store.as_retriever(search_kwargs={"k": 4})

    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.3
    )

    if session_id not in session_histories:
        session_histories[session_id] = []

    chat_history = session_histories[session_id]

    prompt = PromptTemplate.from_template("""
You are a helpful assistant. Use the following document context to answer the question.
If you don't know the answer, say you don't know.

Chat History:
{chat_history}

Context:
{context}

Question: {question}

Answer:""")

    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
            "chat_history": lambda _: format_history(chat_history)
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    answer = chain.invoke(question)
    chat_history.append((question, answer))

    return answer


def clear_session(session_id: str):
    if session_id in session_histories:
        del session_histories[session_id]