from rag.config import CHUNK_OVERLAP, CHUNK_SIZE, KNOWLEDGE_BASE, EMBEDDING_MODEL, LLM_MODEL, PROMPT_TEMPLATE
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import tempfile


splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

doc = Document(page_content=KNOWLEDGE_BASE,
                metadata={"source": "langchain_knowledge_base.md"})

chunks = splitter.split_documents([doc])

vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=EMBEDDING_MODEL,
    persist_directory=tempfile.mkdtemp(),
)

retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 2})

def format_docs(docs):
  return "\n\n".join([doc.page_content for doc in docs])

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | PROMPT_TEMPLATE
    | LLM_MODEL
    | StrOutputParser()
)