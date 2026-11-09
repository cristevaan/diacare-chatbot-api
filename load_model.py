import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import tempfile
from dotenv import load_dotenv

# Configuration

load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

EMBEDDING_MODEL = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2")
LLM_MODEL = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

PROMPT_TEMPLATE = ChatPromptTemplate.from_template(
    """
    Answer the question based only on the following context:
    {context}
    Question: {question}
    Answer:
    Make sure to answer in a concise manner, and if you don't know the answer, say that you don't know.
    """
)

KNOWLEDGE_BASE = """
# LangChain Overview
LangChain is an open-source framework designed to simplify the creation of applications using large language models (LLMs). It was created by Harrison Chase in late 2022.

# LangGraph
LangGraph is an extension of LangChain designed for building stateful, multi-actor applications with LLMs, making it highly suitable for creating complex agentic workflows and cyclical graphs.
"""

# Building the RAG Chain

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

llm = LLM_MODEL

prompt = PROMPT_TEMPLATE

def format_docs(docs):
  return "\n\n".join([doc.page_content for doc in docs])

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# testing

def testing():
  # Testing
  questions = [
      "What is Langchain?",
      "Who created Langchain?",
      "what is LangGraph used for?",
      "Who is Satoshi Nakamoto?"
  ]

  print("Basic RAG Demo:\n")
  for q in questions:
    answer = rag_chain.invoke(q)
    print(f"Q: {q}")
    print(f"A: {answer}\n")
    
def testing2():
  questions2 = [
      "who is new president of USA?",
      "who are you?"
  ]

  print("Basic RAG Demo2:\n")
  for q in questions2:
    answer = rag_chain.invoke(q)
    print(f"Q: {q}")
    print(f"A: {answer}\n")
    
# main

if __name__ == "__main__":
  testing()
  testing2()
