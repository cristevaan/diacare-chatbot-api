from datetime import datetime

from rag.config import RETRIEVE_K
from rag.pipeline import get_rag_chain, get_vectorstore


class RAGUnavailableError(Exception):
    """Index/vectorstore tidak bisa disiapkan."""


class UpstreamError(Exception):
    """LLM upstream gagal atau mengembalikan jawaban kosong."""


def answer(query):
    try:
        chain = get_rag_chain()
    except Exception as e:
        raise RAGUnavailableError("gagal menyiapkan chain") from e
    for _ in range(2):
        result = chain.invoke(query)
        if isinstance(result, str) and result.strip():
            return result
    raise UpstreamError("jawaban kosong dari model")


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
