import logging

from fastapi import APIRouter, HTTPException

from api.schemas import ChatRequest, ChatResponse
from rag.service import RAGUnavailableError, UpstreamError, request_chatbot

logger = logging.getLogger("diacare")

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    try:
        return ChatResponse(**request_chatbot(payload.question.strip()))
    except RAGUnavailableError as e:
        logger.exception("gagal menyiapkan RAG")
        raise HTTPException(status_code=503, detail="Layanan sedang disiapkan, coba lagi nanti.") from e
    except UpstreamError as e:
        logger.exception("upstream LLM bermasalah")
        raise HTTPException(status_code=502, detail="Layanan model sedang bermasalah, coba lagi nanti.") from e
