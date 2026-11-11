from rag.config import RETRIEVE_K
from rag.pipeline import get_rag_chain, get_vectorstore


def answer(query):
    return get_rag_chain().invoke(query)


def retrieve(query):
    return get_vectorstore().similarity_search_with_score(query, k=RETRIEVE_K)
