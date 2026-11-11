from datetime import datetime

from rag.config import RETRIEVE_K
from rag.pipeline import get_rag_chain, get_vectorstore


def answer(query):
    return get_rag_chain().invoke(query)


def retrieve(query):
    return get_vectorstore().similarity_search_with_score(query, k=RETRIEVE_K)


def request_chatbot(query):
    user_record = {
        "sender": "user",
        "message": query,
        "timestamp": datetime.now().isoformat(),
    }
    answer_text = answer(query)
    chatbot_record = {
        "sender": "chatbot",
        "message": answer_text,
        "timestamp": datetime.now().isoformat(),
    }
    return {"user": user_record, "chatbot": chatbot_record}
