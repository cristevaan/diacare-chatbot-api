from pydantic import BaseModel, Field


class ChatRecord(BaseModel):
    sender: str
    message: str
    timestamp: str


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, examples=["Apa itu diabetes?"])


class ChatResponse(BaseModel):
    user: ChatRecord
    chatbot: ChatRecord
