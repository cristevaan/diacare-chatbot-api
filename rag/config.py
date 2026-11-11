from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings


load_dotenv()

EMBEDDING_MODEL = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
)
LLM_MODEL = ChatGroq(model="openai/gpt-oss-20b", temperature=0.2)

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
RETRIEVE_K = 6

PROMPT_TEMPLATE = ChatPromptTemplate.from_messages([
    ("system", """Kamu adalah asisten kesehatan yang menjawab pertanyaan seputar diabetes melitus tipe 2 dewasa, berdasarkan pedoman kesehatan Indonesia (PNPK/Kemenkes).

- Jawab dalam Bahasa Indonesia secara langsung dan ringkas; jangan menyebut "konteks", "di atas", atau cara kerja kamu.
- Jika pertanyaan adalah definisi atau pengetahuan umum dan jawabannya tidak ada di konteks, jawab dengan pengetahuan umum.
- Untuk saran obat, dosis, atau keputusan klinis, hanya gunakan isi konteks; jika tidak ada, arahkan untuk berkonsultasi dengan tenaga medis.
- Jika benar-benar tidak tahu, katakan tidak tahu."""),
    ("human", "{context}\n\nPertanyaan: {question}"),
])