from fastapi import FastAPI

from api.routes import router

app = FastAPI(
    title="Diacare Chatbot API",
    description="Chatbot diabetes melitus tipe 2 berbasis RAG (pedoman PNPK/Kemenkes).",
)
app.include_router(router)
