from fastapi import APIRouter

from api.schemas import ChatRequest, ChatResponse
from rag.service import request_chatbot

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    return ChatResponse(**request_chatbot(payload.question.strip()))
