import pytest

from rag.config import RETRIEVE_K
from rag.pipeline import get_vectorstore
from rag.service import answer, retrieve

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
    result = ""
    for _ in range(2):
        result = answer(question)
        if result.strip():
            break
    assert isinstance(result, str)
    assert result.strip(), "jawaban kosong dari model setelah retry"
