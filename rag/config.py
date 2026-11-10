from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings


load_dotenv()

EMBEDDING_MODEL = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)
LLM_MODEL = ChatGroq(model="openai/gpt-oss-20b", temperature=0.2)

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

PROMPT_TEMPLATE = ChatPromptTemplate.from_template(
    """
    Answer the question based only on the following context:
    {context}
    Question: {question}
    Answer:
    Make sure to answer in a concise manner, using Bahasa Indonesia, and if you don't know the answer, say that you don't know.
    """
)