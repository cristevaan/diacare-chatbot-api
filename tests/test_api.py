from fastapi.testclient import TestClient

from main import app
from rag.service import request_chatbot

client = TestClient(app)


def test_chat_ok(monkeypatch):
    monkeypatch.setattr(
        "api.routes.request_chatbot",
        lambda question: {
            "user": {"sender": "user", "message": question, "timestamp": "2026-11-11T12:00:00"},
            "chatbot": {"sender": "chatbot", "message": f"jawaban untuk {question}", "timestamp": "2026-11-11T12:00:01"},
        },
    )
    response = client.post("/chat", json={"question": "Apa itu diabetes?"})
    assert response.status_code == 200
    body = response.json()
    assert body["user"]["sender"] == "user"
    assert body["user"]["message"] == "Apa itu diabetes?"
    assert body["chatbot"]["sender"] == "chatbot"
    assert body["chatbot"]["message"] == "jawaban untuk Apa itu diabetes?"
    assert body["user"]["timestamp"] and body["chatbot"]["timestamp"]


def test_chat_empty_question(monkeypatch):
    monkeypatch.setattr("api.routes.request_chatbot", lambda question: "tidak boleh dipanggil")
    response = client.post("/chat", json={"question": ""})
    assert response.status_code == 422


def test_request_chatbot_record(monkeypatch):
    monkeypatch.setattr("rag.service.answer", lambda question: "jawaban dummy")
    result = request_chatbot("Apa itu diabetes?")
    assert set(result) == {"user", "chatbot"}
    assert result["user"]["sender"] == "user"
    assert result["chatbot"]["message"] == "jawaban dummy"
    assert result["user"]["timestamp"] and result["chatbot"]["timestamp"]
