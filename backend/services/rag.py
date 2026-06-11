import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

session_histories = {}

BROAD_KEYWORDS = [
    "full",
    "complete",
    "all",
    "entire",
    "summarize",
    "summary",
    "overview",
    "review",
    "everything",
    "overall",
    "explain all",
    "full report",
    "full analysis",
    "full review",
]


def is_broad_question(question: str) -> bool:
    q = question.lower()
    return any(keyword in q for keyword in BROAD_KEYWORDS)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def format_history(history):
    if not history:
        return "No previous conversation."
    result = ""
    for human, ai in history:
        result += f"Human: {human}\nAI: {ai}\n\n"
    return result


def get_all_chunks(vector_store) -> str:
    all_docs = vector_store.docstore._dict.values()
    full_text = "\n\n".join([doc.page_content for doc in all_docs])
    
    if not full_text.strip():
        raise ValueError("Document appears to be empty or could not be read properly.")
    
    return full_text


def ask_question(session_id: str, question: str, summarize: bool = False) -> str:
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small", api_key=os.getenv("OPENAI_API_KEY")
    )

    vector_store = FAISS.load_local(
        f"vector_stores/{session_id}", embeddings, allow_dangerous_deserialization=True
    )

    llm = ChatOpenAI(
        model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"), temperature=0.3
    )

    if session_id not in session_histories:
        session_histories[session_id] = []

    chat_history = session_histories[session_id]

    # Use full document context if summarize=True or broad question detected
    use_full_context = is_broad_question(question)

    prompt = PromptTemplate.from_template("""
    You are an intelligent document assistant. You have been given the COMPLETE document content.
    Provide a thorough, structured, and detailed response.

    Follow these rules:
    - Structure your response with clear sections and headings
    - Use bullet points or numbered lists for multiple items
    - Highlight important findings, key points, or critical values clearly
    - Explain technical terms in simple language
    - Be thorough — do not skip any important information
    - If the document contains data, numbers, or results, interpret and explain what they mean
    - At the end, add a short Summary
    - If something is not found in the document, clearly say so
    - If user says thanks or give any compliment, respond politely but do not add any new information.
    - If the file has not much content and the question is broad, answer based on the limited content but also mention that the document has limited information, not respond with fabricated details.

    Chat History:
    {chat_history}

    Context:
    {context}

    Question: {question}

    Answer:""")

    if use_full_context:
        # If it's a broad question, use the entire document content
        full_text = get_all_chunks(vector_store)
        context = lambda _:full_text
        print("Using full document context for broad question.")
    else:
        # RAG — only fetch top k relevant chunks
        retriever = vector_store.as_retriever(search_kwargs={"k": 4})
        context = retriever | format_docs
        print("Using RAG with top 4 relevant chunks.")

    chain = (
        {
            "context": context,
            "question": RunnablePassthrough(),
            "chat_history": lambda _: format_history(chat_history),
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
