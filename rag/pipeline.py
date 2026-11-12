import os

from rag.config import CHROMA_DIR, CHUNK_OVERLAP, CHUNK_SIZE, EMBEDDING_MODEL, PROMPT_TEMPLATE, RETRIEVE_K, get_llm
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

from rag.doc_loader import load_all_docs


splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

_vector_store = None
_rag_chain = None


def build_index():
    docs = load_all_docs()
    chunks = splitter.split_documents(docs)
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=EMBEDDING_MODEL,
        persist_directory=CHROMA_DIR,
    )
    return vector_store


def get_vectorstore():
    global _vector_store
    if _vector_store is None:
        if os.path.isdir(CHROMA_DIR) and os.listdir(CHROMA_DIR):
            _vector_store = Chroma(persist_directory=CHROMA_DIR, embedding_function=EMBEDDING_MODEL)
        else:
            _vector_store = build_index()
    return _vector_store


def get_retriever():
    return get_vectorstore().as_retriever(search_type="similarity", search_kwargs={"k": RETRIEVE_K})

def format_docs(docs):
  return "\n\n".join([doc.page_content for doc in docs])


def get_rag_chain():
    global _rag_chain
    if _rag_chain is None:
        _rag_chain = (
            {"context": get_retriever() | format_docs, "question": RunnablePassthrough()}
            | PROMPT_TEMPLATE
            | get_llm()
            | StrOutputParser()
        )
    return _rag_chain


if __name__ == "__main__":
    build_index()
    print(f"Index rebuilt at {CHROMA_DIR}")
