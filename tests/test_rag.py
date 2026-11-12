import pytest

from rag.config import RETRIEVE_K
from rag.pipeline import get_vectorstore
from rag.service import UpstreamError, answer, retrieve

QUESTIONS = [
    "Apa yang kamu tahu?",
    "Apa itu diabetes?",
    "Bagaimana cara mengelola diabetes?",
]


@pytest.fixture(scope="module")
def vectorstore():
    return get_vectorstore()


def test_retrieve(vectorstore):
    results = retrieve(QUESTIONS[1])
    assert 0 < len(results) <= RETRIEVE_K
    for doc, score in results:
        assert isinstance(doc.page_content, str)
        assert isinstance(score, float)


@pytest.mark.parametrize("question", QUESTIONS)
def test_answer(question):
    result = answer(question)
    assert isinstance(result, str)
    assert result.strip(), "jawaban kosong dari model setelah retry"


def test_answer_empty_raises(monkeypatch):
    class DummyChain:
        def __init__(self):
            self.calls = 0

        def invoke(self, query):
            self.calls += 1
            return ""

    chain = DummyChain()
    monkeypatch.setattr("rag.service.get_rag_chain", lambda: chain)
    with pytest.raises(UpstreamError):
        answer("Apa itu diabetes?")
    assert chain.calls == 2


def test_answer_retries_once(monkeypatch):
    class DummyChain:
        def __init__(self):
            self.calls = 0

        def invoke(self, query):
            self.calls += 1
            return "" if self.calls == 1 else "jawaban"

    chain = DummyChain()
    monkeypatch.setattr("rag.service.get_rag_chain", lambda: chain)
    assert answer("Apa itu diabetes?") == "jawaban"
    assert chain.calls == 2
